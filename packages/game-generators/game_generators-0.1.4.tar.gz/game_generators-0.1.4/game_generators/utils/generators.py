import numpy as np


def decreasing_sequence(num, batch_size=1, squeeze=False, min_r=0, max_r=5, rng=None, seed=None):
    """Generates a decreasing array across the last dimension.

    Note:
        This is equivalent to generating batch_size number of decreasing functions but is more efficient.

    Args:
        num (int): The number of arrays to generate.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        list: A list of arrays.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    sequences = rng.uniform(size=(batch_size, num))
    sequences = np.cumsum(sequences, axis=-1)
    sequences = sequences / np.max(sequences, axis=-1, keepdims=True)
    sequences = min_r + (max_r - min_r) * sequences
    sequences = np.flip(sequences, axis=-1).swapaxes(0, 1)
    return sequences if squeeze else sequences[..., None]


def coordinate_grid(shape):
    """Generate a coordinate grid.

    Args:
        shape (Tuple[int]): The shape of the grid.

    Returns:
        np.ndarray: The coordinate grid.
    """
    indices = np.expand_dims(np.indices(shape), axis=-1)
    return np.concatenate(indices, axis=-1)
