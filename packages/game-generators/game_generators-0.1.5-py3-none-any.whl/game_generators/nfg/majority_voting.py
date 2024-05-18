import numpy as np


def majority_voting(num_players, num_candidates, batch_size=1, min_r=0, max_r=5, rng=None, seed=None):
    """Generate a majority voting game.

    In this version of the Majority Voting Game, players’ utilities for each candidate (i.e. action) being declared the
    winner are arbitrary and it is possible that a player would be indifferent between two or more candidates. If
    multiple candidates have the same number of votes and this number is higher than the number of votes any other
    candidate has, then the candidate with the lowest number is declared winner.

    Args:
        num_players (int): The number of players.
        num_candidates (int): The number of candidates.
        batch_size (int, optional): The batch size. Defaults to 1.
        min_r (int, optional): The minimum reward. Defaults to 0.
        max_r (int, optional): The maximum reward. Defaults to 5.
        rng (np.random.Generator, optional): The random number generator. Defaults to None.
        seed (int, optional): The random seed. Defaults to None.

    Returns:
        np.ndarray: A majority voting game.
    """
    rng = rng if rng is not None else np.random.default_rng(seed)

    joint_action_shape = (*[num_candidates] * num_players,)
    utilities = rng.uniform(low=min_r, high=max_r, size=(batch_size, num_players, num_candidates))
    payoff_matrices = np.zeros((batch_size, num_players, *joint_action_shape))

    for idx in np.ndindex(*joint_action_shape):
        bincounts = np.bincount(idx)
        winner = np.argmax(bincounts)
        for player in range(num_players):
            payoff_matrices[(slice(None), player) + idx] = utilities[:, player, winner]

    if batch_size == 1:
        return payoff_matrices[0]

    return payoff_matrices
