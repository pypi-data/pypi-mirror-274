import numpy as np
from game_generators.functions.interpolate import interpolate_table
from game_generators.utils.transforms import scale_array


def fill_with_cumsum(dim, rng, max_grad=5, batch_size=1, num_points=10):
    """Fill a table with increasing values using the cumsum method.

    Args:
        dim (int): The dimension of the table.
        rng (np.random.Generator): The random number generator.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        batch_size (int, optional): The batch size. Defaults to 1.
        num_points (int, optional): The number of points. Defaults to 10.

    Returns:
        np.ndarray: The table of increasing values.
    """
    values = rng.uniform(low=0, high=max_grad, size=(batch_size, *([num_points] * dim)))

    for d in range(dim):
        values = values.cumsum(axis=d + 1)
    return values


def fill_with_max_add(dim, rng, max_grad=5, batch_size=1, num_points=10):
    """Fill a table with increasing values using the max add method.

    Args:
        dim (int): The dimension of the table.
        rng (np.random.Generator): The random number generator.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        batch_size (int, optional): The batch size. Defaults to 1.
        num_points (int, optional): The number of points. Defaults to 10.

    Returns:
        np.ndarray: The table of increasing values.
    """
    # Sample the values
    grid_shape = (num_points,) * dim
    grads = rng.uniform(low=0, high=max_grad, size=(batch_size, *grid_shape))
    values = np.zeros((batch_size, *grid_shape))
    padding = ((0, 0), *((1, 0),) * dim)
    padded = np.pad(values, padding, mode="constant", constant_values=0)

    # Iterate over the indices and add the gradient to the maximum of the lower bounds.
    for base_idx in np.ndindex(grid_shape):
        idx = tuple([i + 1 for i in base_idx])
        lower_bounds = []
        for d in range(dim):
            constraint_idx = tuple([idx[i] if i != d else idx[i] - 1 for i in range(dim)])
            lower_bounds.append(padded[:, constraint_idx])
        padded[(slice(None),) + idx] = np.max(lower_bounds) + grads[(slice(None),) + base_idx]

    values = padded[(slice(None),) + (slice(1, None),) * dim]  # Remove the padding
    return values


def increasing_table(
    dim, max_grad=5, method="cumsum", batch_size=1, min_y=0, max_y=10, num_points=10, rng=None, seed=None
):
    """Create a table of increasing values.

    Args:
        dim (int): The dimension of the table.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        method (str, optional): The method to use. Should be either 'cumsum' or 'max_add', Defaults to 'cumsum'.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_y (int, optional): The minimum value. Defaults to 0.
        max_y (int, optional): The maximum value. Defaults to 10.
        num_points (int, optional): The number of points. Defaults to 10.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: The table of increasing values.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    if method == "cumsum":
        values = fill_with_cumsum(dim, rng, max_grad=max_grad, batch_size=batch_size, num_points=num_points)
    elif method == "max_add":
        values = fill_with_max_add(dim, rng, max_grad=max_grad, batch_size=batch_size, num_points=num_points)
    else:
        raise ValueError(f"Invalid method: {method}")

    # Extract the minimum and maximum values for each batch.
    min_values = values[(slice(None),) + ((0,) * dim)].reshape(batch_size, *([1] * dim))
    max_values = values[(slice(None),) + ((-1,) * dim)].reshape(batch_size, *([1] * dim))

    # Scale the table to the desired range
    return scale_array(values, min_values, max_values, min_y, max_y)


def decreasing_table(
    dim, max_grad=5, method="cumsum", batch_size=1, min_y=0, max_y=10, num_points=10, rng=None, seed=None
):
    """Create a table of decreasing values.

    Args:
        dim (int): The dimension of the table.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        method (str, optional): The method to use. Should be either 'cumsum' or 'max_add', Defaults to 'cumsum'.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_y (int, optional): The minimum value. Defaults to 0.
        max_y (int, optional): The maximum value. Defaults to 10.
        num_points (int, optional): The number of points. Defaults to 10.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: The table of decreasing values.
    """
    values = -increasing_table(
        dim,
        max_grad=max_grad,
        method=method,
        batch_size=batch_size,
        min_y=min_y,
        max_y=max_y,
        num_points=num_points,
        rng=rng,
        seed=seed,
    )
    return values + (max_y - min_y)


def increasing(
    dim,
    max_grad=5,
    method="cumsum",
    min_vec=None,
    max_vec=None,
    min_y=0,
    max_y=10,
    batch_size=1,
    batched=True,
    num_points=10,
    rng=None,
    seed=None,
):
    """Create an increasing function.

    Args:
        dim (int): The dimension of the function.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        method (str, optional): The method to use. Should be either 'cumsum' or 'max_add', Defaults to 'cumsum'.
        min_vec (np.array, optional): The minimum input values. Defaults to None.
        max_vec (np.array, optional): The maximum input values. Defaults to None.
        min_y (int, optional): The minimum value. Defaults to 0.
        max_y (int, optional): The maximum value. Defaults to 10.
        batch_size (int, optional): The batch size. Defaults to 1.
        batched (bool, optional): Whether the function is batched or not. Defaults to True.
        num_points (int, optional): The number of points. Defaults to 10.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        callable: An increasing function.
    """
    values = increasing_table(
        dim,
        max_grad=max_grad,
        method=method,
        batch_size=batch_size,
        min_y=min_y,
        max_y=max_y,
        num_points=num_points,
        rng=rng,
        seed=seed,
    )
    batched = batch_size > 1 or batched
    if not batched:
        values = values[0]
    increasing_f = interpolate_table(values, min_vec=min_vec, max_vec=max_vec, batched=batched, method="linear")
    return increasing_f


def decreasing(
    dim,
    max_grad=5,
    method="cumsum",
    min_vec=None,
    max_vec=None,
    min_y=0,
    max_y=10,
    batch_size=1,
    batched=True,
    num_points=10,
    rng=None,
    seed=None,
):
    """Create a decreasing function.

    Args:
        dim (int): The dimension of the function.
        max_grad (int, optional): The maximum gradient used in sampling. This is not guaranteed to be the maximum
            gradient in the final table. Defaults to 5.
        method (str, optional): The method to use. Should be either 'cumsum' or 'max_add', Defaults to 'cumsum'.
        min_vec (np.array, optional): The minimum input values. Defaults to None.
        max_vec (np.array, optional): The maximum input values. Defaults to None.
        min_y (int, optional): The minimum value. Defaults to 0.
        max_y (int, optional): The maximum value. Defaults to 10.
        batch_size (int, optional): The batch size. Defaults to 1.
        batched (bool, optional): Whether the function is batched or not. Defaults to True.
        num_points (int, optional): The number of points. Defaults to 10.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        callable: A decreasing function.
    """
    values = decreasing_table(
        dim,
        max_grad=max_grad,
        method=method,
        batch_size=batch_size,
        min_y=min_y,
        max_y=max_y,
        num_points=num_points,
        rng=rng,
        seed=seed,
    )
    batched = batch_size > 1 or batched
    if not batched:
        values = values[0]
    decreasing_f = interpolate_table(values, min_vec=min_vec, max_vec=max_vec, batched=batched, method="linear")
    return decreasing_f
