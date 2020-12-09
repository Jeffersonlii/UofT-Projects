"""
CSCC11 - Introduction to Machine Learning, Fall 2020, Exam
B. Chan, D. Fleet
"""

import matplotlib.pyplot as plt
import numpy as np
import time

from matplotlib import gridspec

CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']


class EMLineFitting():
    def __init__(self, x, y, K, variances=None, visualize=True):
        """ This class represents the EM algorithm for fitting multiple lines to the 
        observations.

        TODO: Implement the methods of this class:
        - _e_step: ndarray, ndarray -> ndarray
        - _m_step: ndarray, ndarray -> ndarray

        Implementation description will be provided under each method.
        
        For the following:
        - N: Number of samples.
        - K: Number of mixture components

        Args:
        - x (ndarray (shape: (N, 1))): A N-column vector consisting of the x part (input) of the observed data.
        - y (ndarray (shape: (N, 1))): A N-column vector consisting of the y part (output) of the observed data.
        - K (int): Number of mixture components (number of linear models)
        - variances (ndarray (shape: (K, 1))): K-column vector storing the noise variance for component likelihood
        - visualize (bool): Whether or not to visualize the line fitting results.
        """

        # We are fitting lines so both x is a scalar input and y is a scalar output
        assert x.shape == y.shape, f"You must provide x and y with same shape. Got: x - {x.shape}, y - {y.shape}"
        assert len(x.shape) == 2 and x.shape[1] == 1, f"You must provide column vectors. Got: {x.shape}"
        assert variances is None or variances.shape == (K, 1), f"You must provide variances with {K} components. Got: {variances.shape}"

        # Number of observations
        self.N = x.shape[0]

        # Number of mixture components
        self.K = K

        # Each model is a linear model, where the parameter is represented by [b, w]^T
        # All model parameters are randomly initialized
        self.model_parameters = np.empty(shape=(2, self.K))

        # Offset
        self.model_parameters[0, :] = np.random.uniform(-3.0, 3.0, size=self.K)

        # Slope
        self.model_parameters[1, :] = np.random.uniform(-1.0, 1.0, size=self.K)

        # Create array to hold ownership probabilities
        self.ownership_probs = np.zeros(shape=(self.N, self.K))

        # To begin, set mixture probability to be uniform.
        self.mixing_probs = np.ones(shape=(self.K, 1)) / self.K

        self.variances = variances
        if self.variances is None:
            self.variances = np.ones(shape=(self.K, 1))

        # Figures for plotting
        self.visualize = visualize
        self.fig = plt.figure(figsize=(16, 8))
        self.gs = gridspec.GridSpec(self.K, 2, width_ratios=[1, 1], height_ratios=[1 for _ in range(self.K)])
        self.axs = [plt.subplot(self.gs[:, 0])]
        self.axs.extend(plt.subplot(self.gs[plot_i, 1]) for plot_i in range(self.K))

        # Pad 1's to first column to account for the bias (offset).
        padded_x = np.concatenate((np.ones(shape=(self.N, 1)), x), axis=1)

        # Run the EM algorithm on instantiation to fit the lines 
        self._fit(padded_x, y)

    def _e_step(self, x, y):
        """ This method runs the E-step of the EM algorithm. For each input output pair in (x, y), it
        computes the ownership probabilities q_k, for all k = 1 to K.

        NOTE: In this code, index starts at 0 instead of 1.

        Args:
        - x (ndarray (shape: (N, 2))): A Nx2 matrix consisting of the x-component of the observed data 
                                       with 1 padded onto the first column (to allow for bias in regression).
        - y (ndarray (shape: (N, 1))): A N-column vector consisting of the y-component of the observed data.

        Output:
        - ownership_probs (shape: (N, K)): A NxK matrix storing the ownership probabilities.
        - y_pred (ndarray (shape: (N, K))): A NxK matrix storing predictions where each row corresponds to a 
                                            data point being fed to the K linear models.
                                            NOTE: This is only for visualization.
        """

        # ====================================================
        # TODO: Implement your solution within the box

        # ====================================================

        assert ownership_probs.shape == (self.N, self.K), f"ownership_probs shape mismatch. Expected: {(self.N, self.K)}. Got: {ownership_probs.shape}"
        return ownership_probs, y_pred
    
    def _m_step(self, x, y):
        """ This method runs the M-step of the EM algorithm. It computes the parameters of every 
        linear model by minimizing the weighted squared error.

        Args:
        - x (ndarray (shape: (N, 2))): A Nx2 matrix storing x inputs from the observed data 
                                       with 1 padded onto the first column.
        - y (ndarray (shape: (N, 1))): A N-column vector storing of the y values for observed data

        Output:
        - parameters (shape: (K, 2)): A Kx2 matrix storing the parameters of the K mixture components (the linear models)
        - mixing_probs (shape: (K, 1)): A K-column vector storing the mixing probabilities.
        """

        # ====================================================
        # TODO: Implement your solution within the box

        # ====================================================

        assert parameters.shape == (2, self.K), f"parameters shape mismatch. Expected: {(2, self.K)}. Got: {parameters.shape}"
        assert mixing_probs.shape == (self.K, 1), f"mixing_probs shape mismatch. Expected: {(self.K, 1)}. Got: {mixing_probs.shape}"
        return parameters, mixing_probs

    def _fit(self, x, y):
        """ This method fits K linear models to the observation data (x_i, y_i), for i = 1 to N 
        using EM algorithm.

        Args:
        - x (ndarray (shape: (N, 2))): A Nx2 matrix consisting of the x-component of the observation data 
                                       with 1 padded onto the first column.
        - y (ndarray (shape: (N, 1))): A N-column vector consisting of the y-component of the observation data.
        """

        num_iterations = 0
        labels = -np.ones(shape=(self.N, self.K), dtype=np.float)
        while True:
            # E-Step
            self.ownership_probs, y_pred = self._e_step(x, y)

            # Check convergence
            old_labels = np.copy(labels)
            labels = self.ownership_probs

            # Visualize new lines
            if self.visualize:
                self._visualize(x, y, y_pred, self.ownership_probs)

            if np.allclose(old_labels, labels, rtol=1e-3, atol=1e-5):
                print(f"EM algorithm has converged after {num_iterations} iterations.")
                if self.visualize:
                    plt.show()
                break

            # M-Step
            self.model_parameters, self.mixing_probs = self._m_step(x, y)
            num_iterations += 1

    def _visualize(self, x, y, y_pred, ownership_probs):
        self.axs[0].clear()
        self.axs[0].set_title("EM Line Fitting")
        self.axs[0].set_xlabel("x")
        self.axs[0].set_ylabel("y")
        self.axs[0].scatter(x[:, 1], y, c="black")
        for ii in range(self.K):
            self.axs[0].plot(x[:, 1], y_pred[:, ii], label=f"model {ii + 1}", c=CB_color_cycle[ii])
        self.axs[0].set_xlim(np.min(x) - 1, np.max(x) + 1)
        self.axs[0].set_ylim(np.min(y) - 1, np.max(y) + 1)
        self.axs[0].legend(loc='upper left')

        for plot_i in range(1, self.K + 1):
            self.axs[plot_i].clear()
            self.axs[plot_i].set_title(f"Ownership {plot_i}")
            self.axs[plot_i].set_xlabel("Observation")
            self.axs[plot_i].set_ylabel("Probability")
            self.axs[plot_i].bar(np.arange(len(ownership_probs)), ownership_probs[:, plot_i - 1], color=CB_color_cycle[plot_i - 1])
            self.axs[plot_i].set_xlim(0, len(ownership_probs))
            self.axs[plot_i].set_ylim(0, 1)

        plt.tight_layout()
        plt.pause(0.0001)
