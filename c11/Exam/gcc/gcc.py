"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Exam
B. Chan, D. Fleet
"""

import numpy as np

from utils import softmax


class GCC:
    def __init__(self, num_features, num_classes):
        """ This class represents a Gaussian Class Conditional model.
        NOTE: We assume lables are 0 to K - 1, where K is number of classes.

        TODO: Implement the methods of this class:
        - train: ndarray, ndarray -> None
        - predict: ndarray -> ndarray

        Implementation description will be provided below under each method.
        
        For the following:
        - N: Number of samples.
        - D: Dimension of input features vectors.
        - K: Number of classes.

        We have three parameters to keep track of:
        - self.means (ndarray (shape: (K, D))): Mean for each of K Gaussian likelihoods.
        - self.covariances (ndarray (shape: (K, D, D))): Covariance for each of K Gaussian likelihoods.
        - self.priors (shape: (K, 1))): Prior probabilty of drawing samples from each of K class.

        Args:
        - num_features (int): The number of features in the input vector
        - num_classes (int): The number of classes in the task.
        """

        self.D = num_features
        self.K = num_classes

        # Shape: K x D
        self.means = np.zeros((self.K, self.D))

        # Shape: K x D x D
        self.covariances = np.tile(np.eye(self.D), reps=(self.K, 1, 1))

        # Shape: K x 1
        self.priors = np.ones(shape=(self.K, 1)) / self.K

    def train(self, train_X, train_y):
        """ This trains the parameters of the GCC model, given training data.

        Args:
        - train_X (ndarray (shape: (N, D))): NxD matrix storing N D-dimensional training inputs.
        - train_y (ndarray (shape: (N, 1))): Column vector with N scalar training outputs (labels).
                                             NOTE: train_y is a vector of scalar values. You might represent train_y with one-hot encoding.
        """
        assert len(train_X.shape) == len(
            train_y.shape) == 2, f"Input/output pairs must be 2D-arrays. train_X: {train_X.shape}, train_y: {train_y.shape}"
        (N, D) = train_X.shape
        assert N == train_y.shape[
            0], f"Number of samples must match for input/output pairs. train_X: {N}, train_y: {train_y.shape[0]}"
        assert D == self.D, f"Expected {self.D} features. Got: {D}"
        assert train_y.shape[1] == 1, f"train_Y must be a column vector. Got: {train_y.shape}"

        # ====================================================
        for label in range(self.K):
            label_index = list(np.where(train_y == label))[0]
            x_with_label = np.take(train_X, label_index, axis=0)

            # set mean
            self.means[label, :] = np.mean(x_with_label, axis=0)

            # set prior
            self.priors[label] = x_with_label.shape[0] / N

            # set cov
            diff = x_with_label - np.tile(self.means[label, :], (x_with_label.shape[0], 1))  # [x] - [mu]
            diff_m_t = diff[..., None] * diff[:, None, :]  # ([x] - [mu])([x] - [mu])T
            squashed = np.sum(diff_m_t, axis=0)  # \Sigma ([x] - [mu])([x] - [mu])T
            self.covariances[label, :, :] = squashed / (x_with_label.shape[0] - 1)   # ([x] - [mu])([x] - [mu])T / m
        # ====================================================

        assert self.means.shape == (
            self.K, self.D), f"means shape mismatch. Expected: {(self.K, self.D)}. Got: {self.means.shape}"
        assert self.covariances.shape == (self.K, self.D,
                                          self.D), f"covariances shape mismatch. Expected: {(self.K, self.D, self.D)}. Got: {self.covariances.shape}"
        assert self.priors.shape == (
            self.K, 1), f"priors shape mismatch. Expected: {(self.K, 1)}. Got: {self.priors.shape}"

    def predict(self, X):
        """ This computes the probability of each class given X, a matrix of input vectors.

        Args:
        - X (ndarray (shape: (N, D))): NxD matrix with N D-dimensional inputs.

        Output:
        - probs (ndarray (shape: (N, K))): NxK matrix storing N K-vectors (i.e. the K class probabilities)
        """
        assert len(X.shape) == 2, f"Input/output pairs must be 2D-arrays. X: {X.shape}"
        (N, D) = X.shape
        assert D == self.D, f"Expected {self.D} features. Got: {D}"

        logits = np.zeros((N, self.K))

        # ====================================================

        def multivariate_normal_pdf(x, mean, cov):
            inv = np.reciprocal(np.sqrt(np.power(6.28318530718, x.shape[0]) * np.linalg.det(cov)))
            ex = np.e ** (-1 / 2 * (x - mean).T @ np.linalg.inv(cov) @ (x - mean))
            return inv * ex

        for row in range(N):  # loop over each datapoint
            posts = np.zeros((self.K, 1))
            for i in range(self.K):
                posts[i, :] = multivariate_normal_pdf(X[row, :],
                                                      self.means[i, :],
                                                      self.covariances[i, :, :]) * self.priors[i, :]
            for i in range(self.K):
                logits[row, i] = posts[i, :]

        # ====================================================

        probs = softmax(logits)
        return probs
