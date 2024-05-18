import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from game_generators.functions.concave import concave_table, concave
from game_generators.functions.monotonic import decreasing_table, decreasing


def plot_1D_table_function(table_function):
    """Plot a table function.

    Args:
        table_function (np.array): A table function.
    """
    x = np.arange(table_function.shape[0])
    plt.plot(x, table_function)
    plt.show()


def plot_1D_function(f, min_x=0, max_x=10, num_points=100):
    """Plot a table function.

    Args:
        f (function): A function.
        min_x (float, optional): The minimum x value. Defaults to 0.
        max_x (float, optional): The maximum x value. Defaults to 10.
        num_points (int, optional): The number of points to plot. Defaults to 100.
    """
    x = np.linspace(min_x, max_x, num=num_points)
    plt.plot(x, f(x))
    plt.show()


def plot_2D_table_function(table_function):
    """Plot a 2D table function.

    Args:
        table_function (np.array): A 2D table function.
    """
    x = np.array(list(product(*[range(atoms) for atoms in table_function.shape])))
    fx = [table_function[tuple(coords)] for coords in x]

    # Plot a scatter plot where the color is the value of the function
    plt.scatter(x[:, 0], x[:, 1], c=fx, cmap="viridis")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    seed = 1
    num_points_table = 20
    num_points_f = 1000

    # Plot a 1D concave function.
    dim = 1
    f = concave(dim, batch_size=1, batched=False, num_points=num_points_table, seed=seed)
    plot_1D_function(f, min_x=0, max_x=num_points_table - 1, num_points=num_points_f)

    # Plot a 2D concave function.
    dim = 2
    batch_f_2D = concave_table(dim, batch_size=1, num_points=num_points_table, seed=seed)
    f_2D = batch_f_2D[0]
    plot_2D_table_function(f_2D)

    # Plot a 1D decreasing function.
    dim = 1
    f = decreasing(dim, batched=False, num_points=num_points_table, seed=seed)
    plot_1D_function(f, min_x=0, max_x=num_points_table - 1, num_points=num_points_f)

    # Plot a 2D decreasing function.
    dim = 2
    batch_f_2D = decreasing_table(dim, batch_size=1, num_points=num_points_table, seed=seed)
    plot_2D_table_function(f_2D)
