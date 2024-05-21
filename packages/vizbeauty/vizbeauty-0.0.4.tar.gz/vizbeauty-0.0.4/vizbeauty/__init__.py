"""Top-level package for VizBeauty."""

__author__ = """Cristian Del Gobbo"""
__email__ = "cristiandelgobbo87@gmail.com"
__version__ = "0.0.4"
from .common import print_statistic, pearson_correlation
from .vizbeauty import beautybar, reg_scatter, visualize_hyperparameter

__all__ = [
    "print_statistic",
    "pearson_correlation",
    "beautybar",
    "reg_scatter",
    "visualize_hyperparameter"
]

