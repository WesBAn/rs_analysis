import typing

from matplotlib import pyplot as plt
import numpy as np


def get_points(arr: np.array) -> typing.Tuple[np.array, np.array]:
    x_points = np.array([point[0] for point in arr])
    y_points = np.array([point[1] for point in arr])
    return x_points, y_points


def plot_points(
        arr: np.array, title="Points", xlabel="X", ylabel="Y"
):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(*get_points(arr), s=10)
    plt.show()


def plot_piecewise(arr: np.array):
    plt.title("Piecewise")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(*get_points(arr))
    plt.show()


def linear_result_plot(arr: np.array):
    plt.title("Herst dim with line")
    plt.xlabel("X")
    plt.ylabel("Y")
    x, y = get_points(arr)
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(x, y, 'yo', x, poly1d_fn(x), '--k')
    plt.show()
