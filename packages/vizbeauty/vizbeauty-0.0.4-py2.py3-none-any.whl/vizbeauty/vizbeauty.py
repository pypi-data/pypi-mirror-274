"""Main module."""

import seaborn as sns
import matplotlib.pyplot as plt

def beautybar(x, y, data, data_avg, color="skyblue", ax=None):
    """
    Create a bar plot with annotations for each bar and a horizontal line indicating the general average value
    of the variable plotted on the y-axis.

    Parameters:
        x (str): The name of the variable to be plotted on the x-axis.
        y (str): The name of the variable to be plotted on the y-axis.
        data (DataFrame): The dataframe containing the data to be plotted.
        data_avg (DataFrame): The dataframe containing the average values for the y variable.
        color (str, optional): The color of the bars. Defaults to "skyblue".
        ax (matplotlib.axes.Axes, optional): The axes to plot on. If not provided, a new figure will be created.
    """
    if ax is None:
        ax = plt.gca()

    sns.barplot(x=x, y=y, data=data, color=color, ax=ax)

    for index, value in enumerate(data[y]):
        ax.text(index, value + 0.2, str(round(value, 2)), ha='center', va='bottom')

    avg_variable = data_avg[y].mean()

    ax.axhline(y=avg_variable, color='r', linestyle='--')
    ax.text(9.5, avg_variable + 0.2, f'Average: {round(avg_variable, 2)}', color='red')

    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--')
    plt.tight_layout()

def reg_scatter(x, y, data, hue=None, legend="auto", size=None, sizes=None, ax=None):
    """
    Create a scatter plot with a regression line.

    Parameters:
        x (str): The name of the variable to be plotted on the x-axis.
        y (str): The name of the variable to be plotted on the y-axis.
        data (DataFrame): The dataframe containing the data to be plotted.
        hue (str, optional): Variable in data to map plot aspects to different colors.
        legend ({"auto", "brief", "full"}, optional): How to draw the legend. Defaults to "auto".
        size (str, optional): Grouping variable that will produce points with different sizes.
        sizes (tuple, optional): Tuple of minimum and maximum size values to scale the size variable.
        ax (matplotlib axes, optional): Axes object to draw the plot onto.
    """
    sns.scatterplot(x=x, y=y, data=data, ax=ax, hue=hue, legend=legend, size=size, sizes=sizes)
    sns.regplot(x=x, y=y, data=data, ax=ax, scatter=False, ci=None, line_kws={"color": "black"})

def visualize_hyperparameter(param_name, param_values, scores):
    """
    Visualize the effect of a hyperparameter on model performance.

    Parameters:
        param_name (str): Name of the hyperparameter.
        param_values (list): List of values for the hyperparameter.
        scores (list): List of mean squared error scores corresponding to each hyperparameter value.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(param_values, scores, marker='o')
    plt.title(f"Effect of {param_name} on Model Performance")
    plt.xlabel(param_name)
    plt.ylabel("Mean Squared Error")
    plt.grid(True)
    plt.show()
