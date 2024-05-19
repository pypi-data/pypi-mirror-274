import jax
import jax.numpy as jnp
from jaxtyping import Array, Float, Int


def sarsa(
    q_tm1: Float[Array, " n_actions"],
    a_tm1: Int[Array, ""] | int,
    r_t: Float[Array, ""] | float,
    discount_t: Float[Array, ""] | float,
    q_t: Float[Array, " n_actions"],
    a_t: Int[Array, ""] | int,
    stop_target_gradients: bool = False,
) -> Float[Array, ""]:
    """Calculates the SARSA temporal difference error.

    See "Reinforcement Learning: An Introduction" by Sutton and Barto.
    (http://incompleteideas.net/book/ebook/node64.html.)

    Args:
        q_tm1: Float[Array, " n_actions"] Q-values at time t-1.
        a_tm1: Int[Array, ""] action index at time t-1.
        r_t: Float[Array, ""] reward at time t.
        discount_t: Float[Array, ""] discount factor at time t.
        q_t: Float[Array, " n_actions"] Q-values at time t.
        a_t: Int action index at time t.
        stop_target_gradients: bool indicating whether or not to apply stop gradient to
        targets.
    Returns:
      SARSA temporal difference error.
    """
    target_tm1 = r_t + discount_t * q_t[a_t]
    target_tm1 = jax.lax.select(
        stop_target_gradients, jax.lax.stop_gradient(target_tm1), target_tm1
    )
    return target_tm1 - q_tm1[a_tm1]


def q_learning(
    q_tm1: Float[Array, " n_actions"],
    a_tm1: Int[Array, ""] | int,
    r_t: Float[Array, ""] | float,
    discount_t: Float[Array, ""] | float,
    q_t: Float[Array, " n_actions"],
    stop_target_gradients: bool = False,
):
    """Calculates the Q-learning temporal difference error.

    See "Reinforcement Learning: An Introduction" by Sutton and Barto.
    (http://incompleteideas.net/book/ebook/node65.html.)

    Args:
        q_tm1: Float[Array, " n_actions"] Q-values at time t-1.
        a_tm1: Int[Array, ""] action index at time t-1.
        r_t: Float[Array, ""] reward at time t.
        discount_t: Float[Array, ""] discount factor at time t.
        q_t: Float[Array, " n_actions"] Q-values at time t.
        stop_target_gradients: bool indicating whether or not to apply stop gradient to
        targets.
    Returns:
        Q-learning temporal difference error.
    """

    target_tm1 = r_t + discount_t * jnp.max(q_t)
    target_tm1 = jax.lax.select(
        stop_target_gradients, jax.lax.stop_gradient(target_tm1), target_tm1
    )

    return target_tm1 - q_tm1[a_tm1]
