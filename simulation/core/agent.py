"""
Agent for the Tychism spatial bandit model.

The agent navigates an L x L toroidal grid. At each cell, the encounter
is a Bernoulli coin flip: +1 with probability p(x), -1 with probability
1-p(x). The agent maintains Q-values (running estimates of the coin bias
at each cell) and selects arms via softmax over neighboring cells' Q-values.

The coupling loop:
    Q -> softmax(Q/tau) -> arm -> position -> coin flip -> Q update

The nonlinearity that drives trajectory divergence lives in the softmax
policy, not in the update function (which is linear exponential smoothing).
The discrete {+1, -1} Bernoulli outcome provides an additional amplifier:
two agents at the same cell can get opposite outcomes purely by chance.
"""

import numpy as np
from copy import deepcopy


# Direction vectors for the 5 arms
DIRECTIONS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
    'stay': (0, 0),
}
ARM_NAMES = list(DIRECTIONS.keys())
ARM_VECTORS = np.array([DIRECTIONS[a] for a in ARM_NAMES])  # shape (5, 2)


class Agent:
    """Spatial bandit agent with Bernoulli encounters.

    Parameters
    ----------
    L : int
        Grid side length.
    x0 : tuple of int
        Initial position (row, col).
    tau : float
        Softmax temperature. Controls coupling strength.
        tau -> inf: uniform random (no coupling, TvL limit).
        tau -> 0: greedy (maximum coupling).
    alpha : float
        Learning rate for exponential smoothing of Q-values.
        alpha = 0: no learning (frozen prior).
    q_prior : float
        Initial Q-value for all cells. Default 0.0 (expects fair coin).
    rng : np.random.Generator or int, optional
        Random state for arm selection and coin flips.
    """

    def __init__(self, L, x0, tau=1.0, alpha=0.1, q_prior=0.0, rng=None):
        self.L = L
        self.x = np.array(x0, dtype=int)
        self.tau = tau
        self.alpha = alpha
        self.Q = np.full((L, L), q_prior, dtype=float)
        self.o = 0.0  # cumulative outcome
        self.t = 0    # timestep counter

        if rng is None:
            self.rng = np.random.default_rng()
        elif isinstance(rng, (int, np.integer)):
            self.rng = np.random.default_rng(rng)
        else:
            self.rng = rng

        # History tracking
        self.history = []

        # Intervention state
        self._blocked_arms = set()      # for I_K-
        self._arm_bias = np.zeros(5)    # for I_Kw
        self._forced_encounter = None   # for I_e
        self._alpha_override = None     # for I_U (attenuation)
        self._update_transform = None   # for I_U (redirection)

    def _target(self, arm_idx):
        """Compute target cell for an arm pull, with toroidal wrapping."""
        direction = ARM_VECTORS[arm_idx]
        target = (self.x + direction) % self.L
        return target

    def _available_arms(self):
        """Return indices of arms not blocked by I_K-."""
        return [i for i in range(5) if ARM_NAMES[i] not in self._blocked_arms]

    def select_arm(self):
        """Select an arm via softmax over Q-values of reachable cells.

        The softmax is the nonlinear element that drives trajectory divergence.
        Small Q differences are amplified into large arm selection probability
        differences, especially at low tau.

        Returns
        -------
        arm_idx : int
            Index into ARM_NAMES.
        """
        available = self._available_arms()
        if not available:
            raise RuntimeError("All arms blocked — agent cannot move")

        # Q-values at target cells for available arms
        q_values = np.array([self.Q[tuple(self._target(i))] for i in available])

        # Add external bias (I_Kw) for available arms
        biases = np.array([self._arm_bias[i] for i in available])
        q_biased = q_values + biases

        if self.tau >= 1e6:
            # Effectively infinite temperature: uniform random
            idx = self.rng.integers(len(available))
        else:
            # Softmax
            logits = q_biased / self.tau
            logits -= logits.max()  # numerical stability
            probs = np.exp(logits)
            probs /= probs.sum()
            idx = self.rng.choice(len(available), p=probs)

        return available[idx]

    def step(self, landscape):
        """Execute one full timestep of the coupling loop.

        Q -> softmax -> arm -> position -> coin flip -> Q update

        Parameters
        ----------
        landscape : ndarray[L, L]
            The bias map p(x). Can also be a callable (nonstationary)
            in which case pass landscape(self.t).

        Returns
        -------
        encounter : int
            +1 or -1, the coin flip outcome.
        """
        # Get landscape at current time if nonstationary
        if callable(landscape):
            p_map = landscape(self.t)
        else:
            p_map = landscape

        # (1) Arm selection
        arm_idx = self.select_arm()

        # (2) Position update
        new_x = self._target(arm_idx)
        self.x = new_x

        # (3) Encounter: Bernoulli coin flip
        if self._forced_encounter is not None:
            encounter = self._forced_encounter
            self._forced_encounter = None  # one-shot
        else:
            p = p_map[tuple(self.x)]
            encounter = 1 if self.rng.random() < p else -1

        # (4a) Q-value update (learning)
        alpha = self._alpha_override if self._alpha_override is not None else self.alpha
        if alpha > 0:
            e_for_update = encounter
            if self._update_transform is not None:
                e_for_update = self._update_transform(encounter)
            cell = tuple(self.x)
            self.Q[cell] = (1 - alpha) * self.Q[cell] + alpha * e_for_update

        # (4b) Outcome accumulation
        self.o += encounter

        # Record history
        self.history.append({
            't': self.t,
            'x': self.x.copy(),
            'arm': ARM_NAMES[arm_idx],
            'encounter': encounter,
        })

        self.t += 1

        # Clear one-shot intervention flags
        self._alpha_override = None
        self._update_transform = None

        return encounter

    def clone(self):
        """Deep copy for paired comparison experiments.

        Returns an identical agent that can diverge independently.
        The RNG state is also copied, so without intervention,
        both agents would produce identical trajectories.
        """
        new = deepcopy(self)
        return new

    def get_position_history(self):
        """Return position trajectory as ndarray[T, 2]."""
        if not self.history:
            return np.empty((0, 2), dtype=int)
        return np.array([h['x'] for h in self.history])

    def get_encounter_history(self):
        """Return encounter outcomes as ndarray[T]."""
        return np.array([h['encounter'] for h in self.history])

    def get_q_snapshot(self):
        """Return current Q-map as a copy."""
        return self.Q.copy()
