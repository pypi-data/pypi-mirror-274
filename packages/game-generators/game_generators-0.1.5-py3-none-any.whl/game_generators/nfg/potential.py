import numpy as np
from game_generators.utils.generators import coordinate_grid


def potential(
    num_players, num_actions, potential_funs, batch_size=1, min_r=0, max_r=5, weights=None, rng=None, seed=None
):
    """Create a potential game with a weighted potential function.

    Note:
        A pure strategy equilibrium always exists in a potential game.

    Note:
        The potential function should allow for broadcasting.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.
        potential_funs (list): The potential function.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. This is not the global minimum reward, but rather the  minimum reward
            before uniquely determining the other rewards using the potential function. Defaults to 0.
        max_r (int, optional): The maximum reward. A similar warning as for min_r applies. Defaults to 5.
        weights (np.ndarray, optional): The weights for each player. Defaults to None.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A potential game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)
    weights = np.ones((batch_size, num_players)) if weights is None else weights

    action_shape = (num_actions,) * num_players
    payoff_shape = (batch_size, num_players) + action_shape

    payoff_matrices = np.zeros(shape=payoff_shape)
    coordinates = coordinate_grid(action_shape)
    potentials = np.array([potential_fun(coordinates) for potential_fun in potential_funs])

    for player in range(num_players):
        # Set random starting values for the payoff matrix.
        starting_idcs = [slice(None)] * num_players
        starting_idcs[player] = 0
        init_idcs = (slice(None), player) + tuple(starting_idcs)
        payoff_matrices[init_idcs] = rng.uniform(low=min_r, high=max_r, size=payoff_matrices[init_idcs].shape)
        opp_strats = np.delete(action_shape, player)

        for opp_idx in np.ndindex(*opp_strats):  # Calculate the remaining values using the potential function.
            strat_idcs = list(opp_idx)
            strat_idcs.insert(player, slice(None))  # Indices for the strategies uniquely determined by the potential.

            potential_idx = (slice(None),) + tuple(strat_idcs)  # Indices for the potential.

            comp_idx = list(opp_idx)
            comp_idx.insert(player, slice(0, 1))  # Index for the comparison strategy.

            payoff_comp_idx = (slice(None), player) + tuple(comp_idx)  # Index for the comparison payoff.
            potential_comp_idx = (slice(None),) + tuple(comp_idx)  # Index for the comparison potential.
            new_potentials = potentials[potential_idx]
            comp_potentials = potentials[potential_comp_idx]
            comp_payoffs = payoff_matrices[payoff_comp_idx]

            new_ps = (new_potentials - comp_potentials) / weights[:, player : player + 1] + comp_payoffs
            new_idcs = (slice(None), player) + tuple(strat_idcs)
            payoff_matrices[new_idcs] = new_ps  # Set the payoffs.

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
