import numpy as np
from game_generators.utils.generators import decreasing_sequence


def chicken(batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Creates a 2x2 game of chicken.

    This generates a matrix with payoffs

    b, b c, a
    a, c d, d

    Where a > b > c > d

    Generating for more than 2 players is under n-player chicken.

    Args:
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        ndarray: A game of chicken.
    """
    a, b, c, d = decreasing_sequence(4, batch_size=batch_size, min_r=min_r, max_r=max_r, rng=rng, seed=seed)

    payoff_matrices = np.zeros((batch_size, 2, 2, 2))
    payoff_matrices[:, [0, 1], [1, 0], [0, 1]] = a.reshape(batch_size, -1)
    payoff_matrices[:, [0, 1], [0, 0], [0, 0]] = b.reshape(batch_size, -1)
    payoff_matrices[:, [0, 1], [0, 1], [1, 0]] = c.reshape(batch_size, -1)
    payoff_matrices[:, [0, 1], [1, 1], [1, 1]] = d.reshape(batch_size, -1)

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
