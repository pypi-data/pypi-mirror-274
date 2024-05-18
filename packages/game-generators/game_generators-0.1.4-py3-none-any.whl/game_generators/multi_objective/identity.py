import numpy as np


def identity(num_players, num_actions):
    """Generate an identity game.

    Note:
        An identity game is defined as a game where the vector payoff is the joint strategy.

    References:
        .. [1] Röpke, W., Groenland, C., Rădulescu, R., Nowé, A., & Roijers, D. M. (2023). Bridging the gap between
            single and multi objective games. Proceedings of the 2023 International Conference on Autonomous Agents and
            Multiagent Systems, 224–232.

    Args:
        num_players (int): The number of players.
        num_actions (int): The number of actions.

    Returns:
        np.ndarray: An identity game.
    """
    dim = num_actions * num_players
    strats = np.eye(num_actions)

    identity_game = np.zeros((num_players, *([num_actions] * num_players), dim))
    for idx in np.ndindex(*([num_actions] * num_players)):
        payoff = np.zeros(dim)
        for i, s in enumerate(idx):
            payoff[i * num_actions : (i + 1) * num_actions] = strats[s]
        identity_game[(slice(None),) + idx] = payoff
    return identity_game
