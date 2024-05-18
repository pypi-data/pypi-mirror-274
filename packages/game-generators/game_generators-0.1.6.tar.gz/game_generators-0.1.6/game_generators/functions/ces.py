import numpy as np


def ces(dim, rho=0, min_coef=0.1, max_coef=1.0, normalize=True, seed=None, rng=None):
    """Generate a random CES utility function.

    Note:
        The CES utility function is defined as: :math:`u(x) = \left( \sum_{i=1}^n \alpha_i x_i^{\rho} \right)^{\frac{1}{\rho}}`.
        The Cobb-Douglas function is the limiting case of the CES function as :math:`\rho = 0`.

    Note:
        This function is concave.

    Args:
        dim (int): The dimension of the utility function.
        rho (float, optional): The elasticity of substitution. Defaults to 1.
        min_coef (float, optional): The minimum coefficient. Defaults to 0.1.
        max_coef (float, optional): The maximum coefficient. Defaults to 1.0.
        normalize (bool, optional): Whether to normalize the coefficients. Defaults to True.
        seed (int, optional): The random seed. Defaults to None.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    weights = rng.uniform(low=min_coef, high=max_coef, size=dim)
    if normalize:
        weights /= np.sum(weights)

    def ces_f(x):
        return np.power(np.sum(np.power(weights * x, rho)), 1 / rho)

    return ces_f
