import numpy as np
from itertools import chain, combinations


def congestion(num_players, num_facilities, payoff_funcs, batch_size=1):
    """Create a congestion game.

    In the congestion game, each player chooses a subset from the set of all facilities. Each player then receives a
    payoff which is the sum of payoff functions for each facility in the chosen subset. Each payoff function depends
    only on the number of other players who have chosen the facility. Functions used with this generator should always
    be decreasing in order for the resulting game to meet the criteria for being considered a congestion game.

    Note:
        Congestion games are equivalent to exact potential games and therefore also have a potential function and are
        guaranteed to have a pure Nash equilibrium.

    Note:
        Functions used with this generator should always be decreasing in order for the resulting game to meet the
        criteria for being considered a congestion game.

    Note:
        If performance is a critical issue, consider caching the facility counts and selected facilities arrays. These
        arrays only depend on the size of the game and not the payoff functions.

    Args:
        num_players (int): The number of players.
        num_facilities (int): The number of facilities.
        payoff_funcs (list): The payoff functions for each facility.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A congestion game.
    """
    assert len(payoff_funcs) == batch_size, "The number of payoff functions must match the number of batches."

    if num_facilities > 5:
        import warnings

        warnings.warn(
            "The number of actions is 2 to the power of the number of facilities. The game matrix grows "
            "rapidly at a large numbers of facilities!"
        )

    actions = list(chain.from_iterable(combinations(range(num_facilities), r) for r in range(num_facilities + 1)))[1:]
    num_actions = len(actions)
    facility_counts = np.zeros((num_actions,) * num_players + (num_facilities,), dtype=int)
    selected_facilities = np.zeros((num_players,) + (num_actions,) * num_players + (num_facilities,), dtype=bool)

    for joint_action in np.ndindex(*((num_actions,) * num_players)):
        subset_counts = np.bincount(joint_action, minlength=num_actions)
        for subset, count in enumerate(subset_counts):
            for facility in actions[subset]:
                facility_counts[joint_action + (facility,)] += count
        for player, action in enumerate(joint_action):
            for facility in actions[action]:
                selected_facilities[(player, *joint_action, facility)] = True

    facility_payoffs = np.zeros((batch_size, num_players) + (num_actions,) * num_players + (num_facilities,))
    for batch_idx, funcs in enumerate(payoff_funcs):
        for facility_idx, f in enumerate(funcs):
            payoffs_idx = (batch_idx, slice(None)) + (slice(None),) * num_players + (facility_idx,)
            facility_payoffs[payoffs_idx] = f(facility_counts[..., facility_idx : facility_idx + 1])

    payoff_matrices = np.sum(selected_facilities[None, ...] * facility_payoffs, axis=-1)

    if batch_size == 1:
        return payoff_matrices[0]
    else:
        return payoff_matrices
