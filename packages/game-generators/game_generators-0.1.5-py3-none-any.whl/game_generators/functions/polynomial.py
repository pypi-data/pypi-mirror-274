import numpy as np
from itertools import product


def polynomial(dim, degree, min_coef=0.0, max_coef=5.0, seed=None, rng=None):
    """Generate a random polynomial of degree `degree` with coefficients drawn from a uniform distribution.

    Args:
        dim (int): The dimension of the utility function.
        degree (int): The degree of the polynomial.
        min_coef (float, optional): The minimum coefficient. Defaults to 0.
        max_coef (float, optional): The maximum coefficient. Defaults to 5.
        seed (int, optional): The random seed. Defaults to None.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.

    Returns:
        Callable: A random polynomial.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    # Make all combinations of dim integers that sum to a value less than or equal to degree
    # e.g. dim=2, degree=2 -> [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]
    exponents = np.array(list(product(*[range(degree + 1)] * dim)))
    exponents = exponents[exponents.sum(axis=1) <= degree]
    coefficients = rng.uniform(low=min_coef, high=max_coef, size=len(exponents))

    def poly_f(x):
        return np.dot(x**exponents, coefficients)

    return poly_f
