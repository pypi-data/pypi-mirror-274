import jax.numpy as jnp
from jaxonfunctions.rl.value_learning import q_learning, sarsa


def test_sarsa():
    q_tm1 = jnp.array([0.1, 0.2, 0.3])
    a_tm1 = 1
    r_t = 0.5
    discount_t = 0.9
    q_t = jnp.array([0.2, 0.3, 0.4])
    a_t = 2
    stop_target_gradients = True
    result = sarsa(q_tm1, a_tm1, r_t, discount_t, q_t, a_t, stop_target_gradients)
    assert result == 0.66


def test_q_learning():
    q_tm1 = jnp.array([0.1, 0.2, 0.3])
    a_tm1 = 1
    r_t = 0.5
    discount_t = 0.9
    q_t = jnp.array([0.2, 0.3, 0.4])
    stop_target_gradients = True
    result = q_learning(q_tm1, a_tm1, r_t, discount_t, q_t, stop_target_gradients)
    assert result == 0.66
