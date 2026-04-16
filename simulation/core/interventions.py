"""
Intervention operators for the Tychism spatial bandit model.

Six operators target different nodes of the coupling loop:
    Q -> pi (softmax) -> arm -> position -> coin flip -> Q update

Each operator is defined by which node it modifies and whether
it preserves or breaks the encounter-selection coupling.

Level 0 only: these are described as bandit operations, not evaluated
as "good" or "bad." The paper reports their different dynamical
consequences (divergence profiles), not their ethical status.
"""

import numpy as np


def expand_support(agent, x_new, q_info):
    """I_K+ : Support Expansion

    Set Q-value for a cell the agent hasn't visited.
    Equivalent to providing a 'tip' about an unexplored region.

    The agent's policy now includes this cell in its softmax.
    Coupling is preserved — the agent still decides via its own policy.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    x_new : tuple of int
        Cell (row, col) to set Q for.
    q_info : float
        The Q-value to assign.
    """
    agent.Q[x_new] = q_info


def truncate_support(agent, blocked_arms, duration=1):
    """I_K- : Support Truncation

    Remove arm(s) from the available set. Agent cannot pull
    blocked arms regardless of Q-values.

    Coupling runs on a censored landscape — the agent still selects
    via its own Q, but regions of the action space are eliminated.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    blocked_arms : list of str
        Arm names to block (e.g., ['up', 'left']).
    duration : int
        Number of timesteps to block. Default 1 (one-shot).
        For persistent blocking, call before each step.
    """
    agent._blocked_arms = set(blocked_arms)


def unblock_arms(agent):
    """Clear all arm blocks (restore from I_K-)."""
    agent._blocked_arms = set()


def reshape_weights(agent, bias_vector):
    """I_Kw : Weight Reshaping

    Add external bias to arm selection without changing Q-values.
    The softmax becomes:
        pi'(a) ∝ exp((Q(target(a, x)) + b(a)) / tau)

    Agent still selects probabilistically but the distribution
    is externally skewed. Q remains the agent's own.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    bias_vector : array-like, shape (5,)
        Bias for each arm [up, down, left, right, stay].
    """
    agent._arm_bias = np.array(bias_vector, dtype=float)


def clear_bias(agent):
    """Remove external arm bias (restore from I_Kw)."""
    agent._arm_bias = np.zeros(5)


def determine_encounter(agent, forced_e):
    """I_e : Encounter Determination

    Force the next coin flip outcome, overriding the Bernoulli draw.
    The agent updates Q on imposed data — data their trajectory
    did not generate.

    One-shot: applies to the next step only.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    forced_e : int
        The forced encounter value (+1 or -1).
    """
    agent._forced_encounter = forced_e


def substitute_state(agent, Q_new):
    """I_s : State Substitution

    Replace the agent's Q-map with an externally determined one.
    All subsequent arm selections are driven by the imposed Q.
    The agent's entire learned history is overwritten.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    Q_new : ndarray[L, L]
        The replacement Q-map.
    """
    agent.Q = Q_new.copy()


def attenuate_update(agent, alpha_new=None, transform_fn=None):
    """I_U : Update Attenuation

    Modify the learning rule for the next timestep.

    Three forms:
    - Attenuation: reduce alpha (agent learns less)
    - Redirection: transform encounter before Q update
    - Both: reduce alpha AND transform

    One-shot: applies to the next step only.

    Parameters
    ----------
    agent : Agent
        The agent to intervene on.
    alpha_new : float, optional
        Override learning rate for next step.
    transform_fn : callable, optional
        Function e -> e' applied to encounter before Q update.
        Example: lambda e: 0 (suppress all learning)
        Example: lambda e: -e (invert learning signal)
    """
    if alpha_new is not None:
        agent._alpha_override = alpha_new
    if transform_fn is not None:
        agent._update_transform = transform_fn
