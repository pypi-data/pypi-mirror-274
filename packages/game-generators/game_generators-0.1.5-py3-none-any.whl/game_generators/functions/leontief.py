import numpy as np


def leontief(dim, min_coef=0.1, max_coef=1.0, normalize=True, seed=None, rng=None):
    """Generate a random Leontief utility function.

    Note:
        The Leontief utility function is defined as: :math:`u(x) = \min_{i=1} \{ \frac{x_i}{\alpha_i}, \cdots, \frac{x_n}{\alpha_n} \}`.

    Note:
        This function is concave.

    Args:
        dim (int): The dimension of the utility function.
        min_coef (float, optional): The minimum coefficient. Defaults to 0.1.
        max_coef (float, optional): The maximum coefficient. Defaults to 1.0.
        normalize (bool, optional): Whether to normalize the coefficients. Defaults to True.
        seed (int, optional): The random seed. Defaults to None.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.

    Returns:
        Callable: A random Leontief utility function.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    weights = rng.uniform(low=min_coef, high=max_coef, size=dim)
    if normalize:
        weights /= np.sum(weights)

    def leontief_f(x):
        return np.min(x / weights)

    return leontief_f
