"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Assignment 3
B. Chan, Z. Zhang, D. Fleet
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from utils import load_pickle_dataset

def visualize_2d_data(X, y):
    """ This function generates a 2D scatter plot given the inputs and their corresponding labels.
    Inputs with different classes are represented with different colours.

    Args:
    - X (ndarray (shape: (N, D))): A NxD matrix consisting N D-dimensional inputs.
    - y (ndarray (shape: (N, 1))): A N-column vector consisting N scalar outputs (labels).
    """
    assert len(X.shape) == len(y.shape) == 2, f"Input/output pairs must be 2D-arrays. X: {X.shape}, y: {y.shape}"
    (N, D) = X.shape
    assert N == y.shape[0], f"Number of samples must match for input/output pairs. X: {N}, y: {y.shape[0]}"
    assert D == 2, f"Expected 2 features. Got: {D}"
    assert y.shape[1] == 1, f"Y must be a column vector. Got: {y.shape}"

    # ====================================================
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True, linestyle='-', color='0.75')

    x = X[:, 0]
    y = X[:, 1]
    z = y
    # scatter with colormap mapping to z value
    ax.scatter(x, y, s=20, c=z, marker='o', cmap=cm.jet)

    plt.show()

    # ====================================================


if __name__ == "__main__":
    # Support generic_1, generic_2
    dataset = "generic_1"

    assert dataset in ("generic_1", "generic_2"), f"Invalid dataset: {dataset}"

    dataset_path = f"./datasets/{dataset}.pkl"
    data = load_pickle_dataset(dataset_path)
    visualize_2d_data(data['train_X'], data['train_y'])
