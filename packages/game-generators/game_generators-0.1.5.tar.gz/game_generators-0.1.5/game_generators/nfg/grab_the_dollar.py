import numpy as np
from game_generators.utils.generators import decreasing_sequence


def grab_the_dollar(timesteps, batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Create a game of grab the dollar.

    This generates a matrix with payoffs a > b > c such that when two players pick the same time they receive c and
    otherwise the player with the lowest time receives a and the other receives b.

    Args:
        timesteps (int): The number of timesteps.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A game of grab the dollar.
    """
    a, b, c = decreasing_sequence(3, batch_size=batch_size, min_r=min_r, max_r=max_r, rng=rng, seed=seed)

    payoff_matrices = np.zeros((batch_size, 2, timesteps, timesteps))

    u1, u2 = np.triu_indices(timesteps)
    l1, l2 = np.tril_indices(timesteps)
    d1, d2 = np.diag_indices(timesteps)

    payoff_matrices[:, 0, u1, u2] = a
    payoff_matrices[:, 1, u1, u2] = b
    payoff_matrices[:, 0, l1, l2] = b
    payoff_matrices[:, 1, l1, l2] = a
    payoff_matrices[:, 0, d1, d2] = c
    payoff_matrices[:, 1, d1, d2] = c

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
