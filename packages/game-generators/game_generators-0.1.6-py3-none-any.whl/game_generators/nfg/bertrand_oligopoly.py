import numpy as np


def bertrand_oligopoly(num_players, num_actions, cost_funs, demand_funs, batch_size=1):
    """Creates an instance of a Bertrand Oligopoly using arbitrary cost and demand functions.

    In the Bertrand Oligopoly, each player offering the object at the lowest price p will receive a payoff of
    p * (D(p)/m) − C(D(p)/m), where D is the demand function, C is the cost function, and m is the number of players who
    offered the object at this price.

    Note:
        The demand function should be non-negative and decreasing.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.
        cost_funs (list): The cost function.
        demand_funs (list): The demand function.
        batch_size (int, optional): The batch size. Defaults to 1.

    Returns:
        np.ndarray: A random Bertrand Oligopoly game.
    """
    assert batch_size == len(cost_funs), "There must be one cost function per batch."
    assert batch_size == len(demand_funs), "There must be one demand function per batch."

    demands = {}
    costs = {}

    for price in range(1, num_actions + 1):
        demands[price] = np.array([f([price]) for f in demand_funs])
        costs[price] = {}

        for m in range(1, num_players + 1):
            costs[price][m] = np.array([f(demand / m) for f, demand in zip(cost_funs, demands[price])])

    payoff_matrices = np.zeros((batch_size, num_players, *([num_actions] * num_players)))

    for idx in np.ndindex(*([num_actions] * num_players)):
        min_players = np.nonzero(idx == np.min(idx))[0]
        m = len(min_players)
        min_price = np.min(idx) + 1
        payoffs = min_price * (demands[min_price] / m) - costs[min_price][m][..., None]
        payoff_matrices[(slice(None), min_players) + idx] = payoffs

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
