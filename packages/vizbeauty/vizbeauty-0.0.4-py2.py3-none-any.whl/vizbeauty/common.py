"""The common module contains common functions and classes used by the other modules.
"""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def print_statistic(title, variable):
    """
    Prints descriptive statistics for a given variable.

    Parameters:
    - title (str): Title or label for the variable.
    - variable (Series): Pandas Series containing the variable data.

    Returns:
    - None
    """
    print(f"Statistics for {title}:")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Mean: {round(variable.mean(), 2)}")
    print(f"Median: {round(variable.median(), 2)}")
    print(f"Standard Deviation: {round(variable.std(), 2)}")
    print(f"Minimum: {round(variable.min(), 2)}")
    print(f"Maximum: {round(variable.max(), 2)}")
    print(f"25th Percentile (Q1): {round(np.percentile(variable, 25), 2)}")
    print(f"75th Percentile (Q3): {round(np.percentile(variable, 75), 2)}")
    print(f"Skewness: {round(variable.skew(), 2)}")
    print(f"Kurtosis: {round(variable.kurtosis(), 2)}")
    print(f"Count of Missing Values: {variable.isnull().sum()}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()

def pearson_correlation(x, y):
    """
    Compute the Pearson correlation coefficient for two variables and determine if there is a statistically significant correlation.

    Parameters:
    - x (Series): First variable for correlation.
    - y (Series): Second variable for correlation.

    Returns:
    - None
    """
    correlation_coefficient, p_value = pearsonr(x, y)
    alpha = 0.05

    print("Pearson Correlation Coefficient:", correlation_coefficient)
    print("P-value:", p_value)

    if p_value < alpha:
        print(f"There is a statistically significant correlation between {x.name} and {y.name}.")
    else:
        print(f"There is no statistically significant correlation between {x.name} and {y.name}.")
