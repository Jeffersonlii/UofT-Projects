"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Assignment 4
B. Chan, S. Wei, D. Fleet
"""

import numpy as np

def kmeans_pp(K, train_X):
    """ This function runs K-means++ algorithm to choose the centers.

    Args:
    - K (int): Number of centers.
    - train_X (ndarray (shape: (N, D))): A NxD matrix consisting N D-dimensional input data.

    Output:
    - centers (ndarray (shape: (K, D))): A KxD matrix consisting K D-dimensional centers.
    """
    centers = np.empty(shape=(K, train_X.shape[1]))

    # ====================================================
    print(train_X)
    N = train_X.shape[0]
    centers[0, :] = train_X[np.random.randint(0, N), :] # step 1
    for center_i in range(1, K):

        distances = np.empty(shape=(N, center_i))

        for index, center in enumerate(centers[:center_i, :]): #build distance matrix
            newDistanceCol = np.linalg.norm(train_X - center, axis=1)
            distances[:, index] = newDistanceCol

        min_distances = np.square(np.min(distances, axis=1)) # matrix of di^2
        sum_d = min_distances.sum()
        z = np.random.uniform(low=0.0, high=1.0)

        prob_sum = 0
        for yi, di in enumerate(min_distances):
            prob_sum += di / sum_d

            if prob_sum >= z:
                centers[center_i, :] = train_X[yi, :]
                break
    # ====================================================

    return centers

def random_init(K, train_X):
    """ This function randomly chooses K data points as centers.

    Args:
    - K (int): Number of centers.
    - train_X (ndarray (shape: (N, D))): A NxD matrix consisting N D-dimensional input data.

    Output:
    - centers (ndarray (shape: (K, D))): A KxD matrix consisting K D-dimensional centers.
    """
    centers = train_X[np.random.randint(train_X.shape[0], size=K)]
    return centers
