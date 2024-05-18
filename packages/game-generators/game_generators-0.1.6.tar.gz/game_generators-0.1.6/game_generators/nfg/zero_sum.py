import numpy as np


def zero_sum(num_players, num_actions, batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Creates an instance of a zero-sum game.

    Note:
        The sum of payoffs is zero_like and not necessarily exactly zero.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A random zero-sum game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    num_payoffs = num_actions**num_players
    payoffs = rng.uniform(low=min_r, high=max_r, size=(batch_size, num_payoffs, num_players))

    # Shift the array so that its mean is zero
    payoffs -= np.mean(payoffs, axis=-1, keepdims=True)

    # Scale the array so that its sum is zero
    payoffs -= np.sum(payoffs) / num_players

    # Construct the payoff matrix
    payoff_matrices = (
        np.expand_dims(payoffs, -1).swapaxes(1, 2).reshape((batch_size, num_players, *[num_actions] * num_players))
    )

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
