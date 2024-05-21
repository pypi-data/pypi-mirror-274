import pandas as pd
import matplotlib.pyplot as plt
from phik import resources, report
from phik.report import plot_correlation_matrix

def compute_phik_matrix(encoded_data: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет матрицу PhiK для заданного DataFrame.

    Parameters:
    encoded_data (pd.DataFrame): DataFrame с закодированными признаками.

    Returns:
    pd.DataFrame: Матрица PhiK корреляции.
    """
    interval_cols = list(encoded_data.columns)
    phik_overview = encoded_data.phik_matrix(interval_cols=interval_cols)
    return phik_overview

def plot_phik_correlation_matrix(phik_matrix: pd.DataFrame, color_map="Greens", title="Корреляция признаков", figsize=(20, 10)):
    """
    Строит матрицу PhiK корреляции.

    Parameters:
    phik_matrix (pd.DataFrame): Матрица PhiK корреляции.
    color_map (str): Цветовая схема для построения матрицы.
    title (str): Заголовок графика.
    figsize (tuple): Размер фигуры графика.
    """
    plot_correlation_matrix(phik_matrix.values,
                            x_labels=phik_matrix.columns,
                            y_labels=phik_matrix.index,
                            vmin=0, vmax=1, color_map=color_map,
                            title=title,
                            fontsize_factor=1.5,
                            figsize=figsize)
    plt.tight_layout()
    plt.show()
