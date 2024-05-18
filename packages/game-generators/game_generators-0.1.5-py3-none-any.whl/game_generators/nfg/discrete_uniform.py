import numpy as np


def discrete_uniform(num_players, num_actions, batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Generate game with payoffs drawn from the uniform discrite distribution.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A random uniform game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    payoff_matrices = rng.integers(
        low=min_r, high=max_r, size=(batch_size, num_players, *([num_actions] * num_players))
    )

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
