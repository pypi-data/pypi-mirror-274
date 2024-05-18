import numpy as np
from game_generators.utils.generators import decreasing_sequence


def bach_stravinsky(batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Creates a 2x2 Bach or Stravinsky game.

    This generates a table:

    A, B C, C
    C, C B, A

    or

    C, C B, A
    A, B C, C

    such that either (C < A < B) or (C < B < A).

    Note:
        This game is also known as battle of the sexes.

    Args:
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A battle of the sexes game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    a, b, c = decreasing_sequence(3, batch_size=batch_size, min_r=min_r, max_r=max_r, rng=rng)

    # Randomly swap entries from a and b to ensure that sometimes (C < A < B) and sometimes (C < B < A).
    swap = rng.choice([True, False], size=batch_size)
    a[swap], b[swap] = b[swap], a[swap]

    # Generates of the first form first.
    payoff_matrices = np.zeros((batch_size, 2, 2, 2))
    payoff_matrices[:, [0, 1], [0, 1], [0, 1]] = a.reshape(batch_size, -1)
    payoff_matrices[:, [0, 1], [1, 0], [1, 0]] = b.reshape(batch_size, -1)
    payoff_matrices[:, [0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 1, 0]] = c.reshape(batch_size, -1)

    # Randomly swap the first and second rows.
    swap = rng.choice([True, False], size=batch_size)
    payoff_matrices[swap, :, 0, :], payoff_matrices[swap, :, 1, :] = (
        payoff_matrices[swap, :, 1, :],
        payoff_matrices[swap, :, 0, :],
    )

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
