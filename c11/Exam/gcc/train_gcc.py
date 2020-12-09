"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Exam
B. Chan, D. Fleet
"""

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np

from gcc import GCC
from matplotlib.patches import Ellipse
from utils import accuracy, load_pickle_dataset

def train(train_X,
          train_y,
          test_X,
          test_y):
    """ This function trains a logistic regression model given the data.

    Args:
    - train_X (ndarray (shape: (N, D))): A NxD matrix consisting N D-dimensional training inputs.
    - train_y (ndarray (shape: (N, 1))): A N-column vector consisting N scalar training outputs (labels).
    - test_X (ndarray (shape: (M, D))): A NxD matrix consisting M D-dimensional test inputs.
    - test_y (ndarray (shape: (M, 1))): A N-column vector consisting M scalar test outputs (labels).

    Output:
    - model (Object (GCC)): The trained GCC model.
    - train_accuracy (float): The prediction accuracy of the training set.
    - test_accuracy (float): The prediction accuracy of the testing set.
    """

    # Step 1: Get number of features and number of classes from data to initialize GCC.
    num_features = train_X.shape[1]
    num_classes = len(np.unique(train_y))
    model = GCC(num_features, num_classes)

    # Step 2: Train GCC
    model.train(train_X, train_y)

    # Step 3: Evaluate training performance
    train_probs = model.predict(train_X)
    train_accuracy = accuracy(train_probs, train_y)

    # Step 4: Evaluate test performance
    test_probs = model.predict(test_X)
    test_accuracy = accuracy(test_probs, test_y)

    return model, train_accuracy, test_accuracy

def visualize_results(train_X,
                      train_y,
                      train_acc,
                      test_X,
                      test_y,
                      test_acc,
                      model,
                      n_std=3):
    """ Visualizes the datasets and display the GCC means.

    Args:
    - train_X (ndarray (shape: (N, D))): A NxD matrix consisting N D-dimensional training inputs.
    - train_y (ndarray (shape: (N, 1))): A N-column vector consisting N scalar training outputs (labels).
    - train_acc (float): The prediction accuracy of the training set.
    - test_X (ndarray (shape: (M, D))): A NxD matrix consisting M D-dimensional test inputs.
    - test_y (ndarray (shape: (M, 1))): A N-column vector consisting M scalar test outputs (labels).
    - test_acc (float): The prediction accuracy of the testing set.
    - model (Object (GCC)): The trained GCC model.
    - n_std (int): Number of standard deviations when visualizing the Gaussian.
    """
    labels = np.unique(train_y)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    for class_i in labels:
        axs[0].set_xlim(np.min(train_X[:, 0]) - 1, np.max(train_X[:, 0]) + 1)
        axs[0].set_ylim(np.min(train_X[:, 1]) - 1, np.max(train_X[:, 1]) + 1)
        axs[0].scatter(train_X[train_y.flatten() == class_i, 0], train_X[train_y.flatten() == class_i, 1])

        axs[1].set_xlim(np.min(test_X[:, 0]) - 1, np.max(test_X[:, 0]) + 1)
        axs[1].set_ylim(np.min(test_X[:, 1]) - 1, np.max(test_X[:, 1]) + 1)
        axs[1].scatter(test_X[test_y.flatten() == class_i, 0], test_X[test_y.flatten() == class_i, 1])

    # Plot Gaussians
    # Credit: https://matplotlib.org/3.1.1/gallery/statistics/confidence_ellipse.html#sphx-glr-gallery-statistics-confidence-ellipse-py
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                      '#f781bf', '#a65628', '#984ea3',
                      '#999999', '#e41a1c', '#dede00']
    for ii in range(len(model.means)):
        cov = model.covariances[ii]
        pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        for plot_i in range(2):
            ellipse = Ellipse((0, 0),
                            width=ell_radius_x * 2,
                            height=ell_radius_y * 2,
                            facecolor="none",
                            edgecolor=CB_color_cycle[ii],
                            alpha=0.3)

            scale_x = np.sqrt(cov[0, 0]) * n_std
            scale_y = np.sqrt(cov[1, 1]) * n_std
            transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(model.means[ii, 0], model.means[ii, 1])
            ellipse.set_transform(transf + axs[plot_i].transData)

            axs[plot_i].scatter(model.means[ii, 0], model.means[ii, 1], color=CB_color_cycle[ii], marker="x")
            axs[plot_i].add_patch(ellipse)

    axs[0].set_title(f"Training Set\nAccuracy: {train_acc}%")
    axs[1].set_title(f"Training Set\nAccuracy: {test_acc}%")

    plt.show()


if __name__ == "__main__":
    # Support generic_1, generic_2, generic_3
    dataset = "generic_3"

    assert dataset in ("generic_1", "generic_2", "generic_3"), f"Invalid dataset: {dataset}"

    dataset_path = f"./datasets/{dataset}.pkl"
    data = load_pickle_dataset(dataset_path)

    model, train_acc, test_acc = train(data['train_X'],
                                       data['train_y'],
                                       data['test_X'],
                                       data['test_y'])

    visualize_results(data['train_X'],
                      data['train_y'],
                      train_acc,
                      data['test_X'],
                      data['test_y'],
                      test_acc,
                      model)
