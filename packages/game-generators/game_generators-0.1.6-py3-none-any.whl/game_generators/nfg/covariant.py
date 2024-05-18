import numpy as np


def covariant(num_players, num_actions, batch_size=1, mean=0, std=1, cov=0, rng=None, seed=None):
    """Create a covariant game.

    Creates a game with the given number of players with payoffs drawn from a multivariate normal distribution with a
    given covariance.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.
        batch_size (int, optional): The batch size. Defaults to 1.
        mean (float or array_like, optional): The mean of the normal distribution. Defaults to 0.
        std (float or array_like, optional): The standard deviation of the normal distribution. Defaults to 1.
        cov (float, optional): The covariance of the normal distribution. Defaults to 0.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A covariant game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    if isinstance(mean, (int, float)):
        mean = np.full(num_players, mean)

    cov = np.full((num_players, num_players), cov)
    np.fill_diagonal(cov, std)

    num_payoffs = (num_actions**num_players) * batch_size
    player_payoffs = rng.multivariate_normal(mean, cov, size=num_payoffs)
    payoff_matrices = player_payoffs.T.reshape(num_players, batch_size, *([num_actions] * num_players)).swapaxes(0, 1)

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
