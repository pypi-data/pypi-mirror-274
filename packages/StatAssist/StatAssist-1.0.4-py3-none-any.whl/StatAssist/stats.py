import random
import math
from sklearn.mixture import GaussianMixture
import torch
import torch.nn as nn
import pandas as pd
import numpy as np


class STATS:
    @staticmethod
    def get_mean(*Data: list) -> list:
        """
        Returns the mean for multiple sets of data
        :param Data: list, contains a list of datasets.
        :return: list, Measure of the average of a dataset.

        Example:

        >>> x = [2, 4, 6]
        >>> y = [4, 8, 12]
        >>> z = [...]

        >>> averages = statistics_.get_mean(x, y, ...)
        >>> print(averages)

        Returns: [4, 8, ...]
        """
        means = []
        for dataset in Data:
            temp = 0
            n = len(dataset)
            for datapoint in dataset:
                temp += datapoint / n

            means.append(temp)
        return means

    @staticmethod
    def get_variance(datasets: list, means: list) -> list:
        """
        Returns the variance for multiple datasets.
        :param datasets: list, contains a list of datasets.
        :param means: list, means for each dataset.
        :return: list, Measure of the 'spread' of a dataset.

        Example:

        >>> x = [2, 4, 6]
        >>> y = [4, 8, 12]
        >>> z = [...]
        >>> averages = statistics_.get_mean(x, y, ...)

        >>> Variances = statistics_.get_variance([x, y, ...], averages)
        >>> print(Variances)

        Returns: [0, 0, ...]
        """
        variances = []

        if len(datasets) == len(means):
            for i in range(len(means)):
                n = len(datasets[i])
                temp = 0

                for j in range(n):
                    temp += pow(datasets[i][j] - means[i], 2) / n

                variances.append(temp)

            return variances

        return ["len(datasets) != len(means)"]

    @staticmethod
    def get_covariance(datasets: list, means: list) -> float:
        """
        Obtains the covariance between two datasets, x and y.
        :param datasets: list, [dataset 'x', dataset 'x'].
        :param means: list, ['x' mean, 'y' mean].
        :return: float, covariance for datasets x and y.

        Example:

        >>> x = [2, 4, 6]
        >>> y = [4, 8, 12]
        >>> averages = statistics_.get_mean(x, y)

        >>> cov = statistics_.get_covariance(x, y, averages)
        >>> print(cov)

        Returns: 0
        """
        covariance = 0
        mu_x = means[0]
        mu_y = means[1]
        x = datasets[0]
        y = datasets[1]
        n = len(datasets[0])

        for i in range(n):
            covariance += (x[i] - mu_x) * (y[i] - mu_y) / n

        return covariance

    @staticmethod
    def get_correlation_coefficient(covariance_xy: float, variance_x: float, variance_y: float) -> float:
        """
        Returns the correlation coefficient for dataset x and y.
        :param covariance_xy: float.
        :param variance_x: float.
        :param variance_y: float.
        :return: flaot, measure of correlation between datasets x and y.

        Example:

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)
        >>> cov = statistics_.get_covariance(data, averages)

        >>> corr_coeff = get_corr_coeff(cov, variances[0], variances[1])
        """
        return covariance_xy / math.sqrt(variance_x * variance_y)

    @staticmethod
    def calculate_confidence_interval(data: list, mean: float, variance: float, z: float = 1.96) -> list:
        """
        Calculates the confidence interval for the population.
        :param data: list, the number of datapoints.
        :param mean: float, the average of the data
        :param variance: float, measure of how 'spread-apart' the data is.
        :param z: Z-score associated with the desired confidence level; Default: 1.96 (95%)
        :return: list, Upper bound and lower bound for desired confidence level.

        Example:

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)

        >>> x_confidence_interval = statistics_.calculate_confidence_interval(x_data, averages[0], variances[0])

        """
        pop_size = len(data)
        A = z * math.sqrt(variance / pop_size)

        return [mean - A, mean + A]

    @staticmethod
    def get_linreg_slope(corr_coeff: float, var_x: float, var_y: float) -> float:
        """
        Calculates the slope for a linear regression.
        :param corr_coeff: float, correlation coefficient.
        :param var_x: float, variance for dataset x.
        :param var_y: float, variance for dataset y.
        :return: float, linear regression slope.

        Example

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)
        >>> cov = statistics_.get_covariance(data, averages)

        >>> corr_coeff_ = statistics_.get_correlation_coefficient(cov, variances[0], variances[1])

        >>> slope = statistics_.get_linreg_slope(corr_coeff_, variances[0], variances[1])
        """
        m = corr_coeff * math.sqrt(var_y / var_x)

        return m

    @staticmethod
    def normal(x: float, mean_var: list) -> float:
        """
        Returns an evaluation of the normal distribution at x.
        :param x: float.
        :param mean_var: list, mean/variance
        :return: float.

        Example:

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)

        >>> x_mean_var = [averages[0], variances[0]]

        >>> N = statistics_.normal(x, x_mean_var)
        """
        mu = mean_var[0]
        variance = mean_var[1]

        A = 1 / math.sqrt(2 * math.pi)
        xp = -0.5 * pow(x - mu, 2) / variance

        return A * math.exp(xp)

    def std_normal_prob(self, x: float, mean: float, variance: float) -> float:
        """
        Returns an evaluation of the standard normal distribution at z; given x, mu, and sigma.
        :param x: float.
        :param mean: float
        :param variance, float
        :return: float

        Example:

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)

        >>> prob_of_some_value_in_x_data = statistics_.std_normal_prob(x, averages[0], variances[0])
        """
        mu = mean

        z = (x - mu) / math.sqrt(variance)
        P = 0

        dx = 0.0001
        x = -10000
        while x < z:
            P += self.normal(x, [0, 1]) * dx
            x += dx

        return P

    @staticmethod
    def gamma_dist(x: float, Args: list) -> float:
        """
        Gamma distribution function
        :param x: float, value > 0.
        :param Args: list, [shape param (alpha), scale/stretch param (beta)]; beta > 0
        :return: float
        """
        alpha = Args[1]
        beta = Args[2]

        return pow(beta, alpha)*pow(x, alpha - 1)*math.exp(-beta*x)

    def gamma_prob(self, alpha: float, beta: float, interval: list=[.00001, 10000]) -> float:
        """
        Returns probability on an interval
        :param alpha: float, shape parameter
        :param beta: float, scale/stretch parameter
        :param interval: list, Default: [.00001, 10000]
        :return: float
        """
        P = 0

        dx = 0.0001
        area = 0
        x = interval[0]
        while x < interval[1]:
            area += self.gamma_dist(x, [alpha, beta]) * dx
            x += dx

        return P

    @staticmethod
    def monte_carlo_1(sample_space: list, success: float, num_trials: int = 10000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by exact value.
        :param sample_space: list, contains all historical outcomes.
        :param success: float, only values equal to this value constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000
        :return: float, probability of observing 'success' parameter.

        Example:

        >>> x_data = [10, 10, 10, 10, 10, 8, 8, 8, 11, 11, 11, 2, 2, 15, 15]

        >>> prob_next_observation_is_8 = statistics_.monte_carlo_1(x_data, 8)
        """
        num_success = 0
        for trial in range(num_trials):
            if random.choice(sample_space) == success:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def monte_carlo_2(sample_space: list, success_threshold: float, num_trials: int = 10000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by a threshold value.
        :param sample_space: list, contains all historical outcomes.
        :param success_threshold: float, values greater than or equal to this value constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000
        :return: float, probability of observing values greater than or equal to 'success_threshold' parameter.

        Example:

        >>> x_data = [10, 10, 10, 10, 10, 8, 8, 8, 11, 11, 11, 2, 2, 15, 15]

        >>> prob_next_observation_is_greater_than_or_equal_to_8 = statistics_.monte_carlo_2(x_data, 8)
        """
        num_success = 0
        for trial in range(num_trials):
            if random.choice(sample_space) >= success_threshold:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def monte_carlo_3(sample_space: list, success_interval: list, num_trials: int = 1000) -> float:
        """
        Returns probability via monte carlo method; Success is determined by a success interval.
        :param sample_space: list, contains all historical outcomes.
        :param success_interval: list, values within this interval constitute a success.
        :param num_trials: int, number of times the historical outcomes will be sampled; Default: 1000.
        :return: float, probability of observing values within the 'success_interval' parameter.

        Example:

        >>> x_data = [10, 10, 10, 10, 10, 8, 8, 8, 11, 11, 11, 2, 2, 15, 15]

        >>> prob_next_observation_is_between_8_and_11 = statistics_.monte_carlo_3(x_data, [8, 11])
        """
        num_success = 0
        for trial in range(num_trials):
            if success_interval[0] < random.choice(sample_space) < success_interval[1]:
                num_success += 1

        return num_success / num_trials

    @staticmethod
    def gaussian_mixed_model(data: list, *, n_clusters=1):
        """
        Calculates clusters assuming gaussian distribution.
        :param data: list, list containing any number of same length lists.
        :param n_clusters: int, GMM must assume the number of clusters present; Default: 1.
        :return: data (>70% prob.): list, metadata: class

        Example:

        >>> x_data = [0, 1, 2, 3, 4, 5]
        >>> y_data = [0.8, 1, 0.7, 9, 9.2, 8.5]
        >>> data = [x_data, y_data]

        >>> clusters, metadata = statistics_.gaussian_mixed_model(data, n_clusters=2)
        """
        n_columns = len(data)
        data_points = []
        for i in range(len(data[0])):
            datapoint = []
            for j in range(n_columns):
                datapoint.append(data[j][i])
            data_points.append(datapoint)

        data = np.array(data_points)

        gmm = GaussianMixture(n_components=n_clusters, random_state=31415, max_iter=1000)
        gmm.fit(data)

        labels = gmm.predict(data)
        p = gmm.predict_proba(data)

        COV_ = gmm.__getattribute__('covariances_')
        MU = gmm.__getattribute__('means_').tolist()
        BIC = gmm.bic(data)

        class METADATA:
            @staticmethod
            def covariance_matrix():
                return COV_

            @staticmethod
            def cluster_means():
                return MU

            @staticmethod
            def Bayesian_Information_Criterion():
                return BIC

        metadata = METADATA

        L = data.tolist()
        frame = pd.DataFrame(L)
        frame['cluster'] = labels
        frame['probability'] = p.max(axis=1)

        cols = []
        cols_end = ['cluster', 'probability']
        for i in range(n_columns):
            if i < n_columns:
                cols.append(f'[Column: {i + 1}]')

        frame.columns = cols + cols_end
        threshold = 0.7

        filtered_frame = frame[frame['probability'] > threshold]

        data_assignment = []
        for k in range(n_clusters):
            data_assignment.append(filtered_frame[filtered_frame['cluster'] == k])

        return data_assignment, metadata

    @staticmethod
    def ml_linreg_1(dataset_xy, EPOCH=500, *, slope: float) -> float:
        """
        PyTorch machine learning algorithm for linear regression.
        :param dataset_xy: list, containing two 1-dimensional lists of the same length.
        :param slope: float, known slope of the line.
        :return: float, y-intercept

        Example

        >>> data = [x_data, y_data]

        >>> averages = statistics_.get_mean(x_data, y_data)
        >>> variances = statistics_.get_variance(data, averages)
        >>> cov = statistics_.get_covariance(data, averages)
        >>> corr_coeff_ = statistics_.get_correlation_coefficient(cov, variances[0], variances[1])

        >>> m = statistics_.get_linreg_slope(corr_coeff_, variances[0], variances[1])
        >>> y_intercept = statistics_.ml_linreg_1(data, m)
        """
        x = []
        y = []
        for i in range(len(dataset_xy[0])):
            x.append([dataset_xy[0][1]])
            y.append([dataset_xy[1][1]])

        x = torch.Tensor(x)
        y = torch.Tensor(y)

        b = nn.Parameter(torch.randn(1, 1))
        M = torch.Tensor([slope])
        loss_f = torch.nn.MSELoss(size_average=False)
        optimizer = torch.optim.SGD([b], lr=0.001)

        epoch = 0
        while epoch < EPOCH:
            pred_y = M * x + b
            optimizer.zero_grad()
            loss = loss_f(pred_y, y)
            loss.backward()
            optimizer.step()

            epoch += 1

        return b.item()

    @staticmethod
    def ml_linreg_2(dataset_xy, *, y_intercept):
        """
        PyTorch machine learning algorithm for linear regression.
        :param dataset_xy: list, containing two 1-dimensional lists of the same length.
        :param y_intercept: float, known y-intercept of the line.
        :return: float, slope
        """
        x = []
        y = []
        for i in range(len(dataset_xy[0])):
            x.append([dataset_xy[0][1]])
            y.append([dataset_xy[1][1]])

        x = torch.Tensor(x)
        y = torch.Tensor(y)

        m = nn.Parameter(torch.randn(1, 1))
        B = torch.Tensor([y_intercept])
        loss_f = torch.nn.MSELoss(size_average=False)
        optimizer = torch.optim.SGD([m], lr=0.001)

        epoch = 0
        while epoch < 1500:
            pred_y = m * x + B
            optimizer.zero_grad()
            loss = loss_f(pred_y, y)
            loss.backward()
            optimizer.step()

            epoch += 1

        return m.item()


statistics_ = STATS()
