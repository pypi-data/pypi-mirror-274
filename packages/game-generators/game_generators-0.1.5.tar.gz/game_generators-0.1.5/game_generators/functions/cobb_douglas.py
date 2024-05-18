import numpy as np


def cobb_douglas(dim, min_coef=0.1, max_coef=1.0, normalize=True, seed=None, rng=None):
    """Generate a random Cobb-Douglas utility function.

    Note:
        The Cobb-Douglas utility function is defined as: :math:`u(x) = \prod_{i=1}^n x_i^{\alpha_i}`.

    Note:
        This function is concave when all exponents are greater or equal to zero and their sum is less than or equal to
        one.

    Args:
        dim (int): The dimension of the utility function.
        min_coef (float, optional): The minimum coefficient. Defaults to 0.1.
        max_coef (float, optional): The maximum coefficient. Defaults to 1.0.
        normalize (bool, optional): Whether to normalize the coefficients. Defaults to True.
        seed (int, optional): The random seed. Defaults to None.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.

    Returns:
        Callable: A random Cobb-Douglas utility function.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    exponents = rng.uniform(low=min_coef, high=max_coef, size=dim)
    if normalize:
        exponents /= np.sum(exponents)

    def cobb_douglas_f(x):
        return np.prod(np.power(x, exponents))

    return cobb_douglas_f
