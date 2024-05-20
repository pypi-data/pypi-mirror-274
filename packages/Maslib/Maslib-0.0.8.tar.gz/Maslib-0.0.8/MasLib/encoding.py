from sklearn import preprocessing
import pandas as pd

def number_encode_features(init_df: pd.DataFrame) -> (pd.DataFrame, dict):
    """
    Функция для кодирования категориальных признаков в числовые.

    Parameters:
    init_df (pd.DataFrame): Исходный DataFrame.

    Returns:
    result (pd.DataFrame): DataFrame с закодированными признаками.
    encoders (dict): Словарь с LabelEncoder для каждого категориального признака.
    """
    result = init_df.copy()  # копируем нашу исходную таблицу
    encoders = {}
    for column in result.columns:
        if result.dtypes[column] == object:
            encoders[column] = preprocessing.LabelEncoder()
            result[column] = encoders[column].fit_transform(result[column])
    return result, encoders
