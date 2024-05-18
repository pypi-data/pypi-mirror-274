import numpy as np


def war_of_attrition(timesteps, batch_size=1, min_r=20, max_r=20, min_dec=1, max_dec=3, rng=None, seed=None):
    """Create a game of grab the dollar.

    This generates a matrix with payoffs a > b > c such that when two players pick the same time they receive c and
    otherwise the player with the lowest time receives a and the other receives b.

    Args:
        timesteps (int): The number of timesteps.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        min_dec (int, optional): The minimum decrement. Defaults to 1.
        max_dec (int, optional): The maximum decrement. Defaults to 1.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A game of grab the dollar.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    valuations = (
        rng.uniform(low=min_r, high=max_r, size=(batch_size, 2, 1, 1))
        .repeat(timesteps, axis=2)
        .repeat(timesteps, axis=3)
    )
    decrements = rng.uniform(low=min_dec, high=max_dec, size=(batch_size, 2))

    u1, u2 = np.triu_indices(timesteps, k=1)
    l1, l2 = np.tril_indices(timesteps, k=-1)
    d1, d2 = np.diag_indices(timesteps)

    multipliers = np.tile(np.arange(timesteps), (timesteps, 1))
    min_matrix = np.minimum(multipliers, multipliers.T)
    decrements = decrements[:, :, None, None] * min_matrix[None, :, :]

    valuations[:, 0, u1, u2] = 0
    valuations[:, 1, l1, l2] = 0
    valuations[:, :, d1, d2] /= 2
    valuations -= decrements

    if batch_size == 1:
        return valuations[0]
    else:
        return valuations
