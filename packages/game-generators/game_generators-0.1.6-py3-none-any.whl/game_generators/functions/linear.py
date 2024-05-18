from game_generators.functions.polynomial import polynomial


def linear(dim, min_coef=0.0, max_coef=5.0, seed=None, rng=None):
    """Generate a random linear function with coefficients drawn from a uniform distribution.

    Args:
        dim (int): The dimension of the utility function.
        min_coef (float, optional): The minimum coefficient. Defaults to 0.
        max_coef (float, optional): The maximum coefficient. Defaults to 5.
        seed (int, optional): The random seed. Defaults to None.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.

    Returns:
        Callable: A random polynomial.
    """
    return polynomial(dim, degree=1, min_coef=min_coef, max_coef=max_coef, seed=seed, rng=rng)
