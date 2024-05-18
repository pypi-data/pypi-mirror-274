import os

import numpy as np


def save_games(payoff_matrices, separate=True, path=".", prefix="game"):
    """Save a game or games to disk using the numpy binary format.

    Args:
        payoff_matrices (np.ndarray): The payoff matrices.
        separate (bool, optional): Whether to save each game separately. Defaults to True.
        path (str, optional): The path to save the game(s) to. Defaults to '.'.
        prefix (str, optional): The prefix for the filename(s). Defaults to 'game'.

    Returns:
        None
    """
    suffix = ".npy"

    if separate:
        for i, payoff_matrix in enumerate(payoff_matrices):
            filename = f"{prefix}_{i}{suffix}"
            np.save(f"{path}/{filename}", payoff_matrix)
    else:
        filename = f"{prefix}{suffix}"
        np.save(f"{path}/{filename}", payoff_matrices)


def load_games(path="."):
    """Load a game or games from disk using the numpy binary format.

    Args:
        path (str, optional): The path to load the game(s) from. Defaults to '.'.

    Returns:
        np.ndarray: The payoff matrices.
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        files = [f for f in files if f.endswith(".npy")]
        files = sorted(files, key=lambda x: int(x.split("_")[1].split(".")[0]))
        payoff_matrices = np.array([np.load(f"{path}/{f}") for f in files])
    else:
        payoff_matrices = np.load(path)
    return payoff_matrices
