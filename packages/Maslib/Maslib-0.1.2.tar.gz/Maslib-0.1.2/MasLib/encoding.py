from sklearn import preprocessing
import pandas as pd
import numpy as np
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

def process_column_and_merge(df_main, df_additional, column_name, merge_column):
    """
    Process a specified column of a dataframe to extract values and merge with an additional dataframe.
    
    Parameters:
    df_main (pd.DataFrame): The main dataframe.
    df_additional (pd.DataFrame): The additional dataframe to be merged.
    column_name (str): The name of the column to process.
    merge_column (str): The column to which the processed data will be added in df_main.
    
    Returns:
    pd.DataFrame: The main dataframe with the processed and merged column.
    """
    
    danger = []
    except_value = [np.nan, np.nan]
    
    for row in range(df_main.shape[0]):
        try:
            danger.append(list(df_main[column_name])[row].values())
        except:
            danger.append(except_value)
    
    # Create a DataFrame from the extracted values
    data_points = pd.DataFrame(columns=list(df_additional[column_name])[0].keys(), data=danger)
    
    # Merge the new DataFrame with the main DataFrame
    df_main = pd.concat([df_main, data_points], axis=1)
    
    # Optionally, we could drop the original column if it's no longer needed
    # df_main.drop(columns=[column_name], inplace=True)
    
    return df_main

# Example usage
# df_main = pd.read_csv('path_to_main_dataframe.csv')
# df_additional = pd.read_csv('path_to_additional_dataframe.csv')
# updated_df = process_column_and_merge(df_main, df_additional, 'column_name_to_process', 'merge_column_name')
# print(updated_df.head())

def json_to_dataframe(json_path,name,name1,name3):
    with open(json_path, 'r', encoding='utf-8') as f:
        target = json.load(f)
    df_json = pd.DataFrame(target[name])
    dict1 = {}
    for company, nomination in zip(df_json[name2], df_json[name3]):
        dict1[company] = nomination
    return df_json, dict1

# Пример использования:
# df_main = pd.read_csv('path_to_main_dataframe.csv')
# df_additional = pd.read_csv('path_to_additional_dataframe.csv')
# df_main = process_column_and_merge(df_main, df_additional, 'point', 'merge_column')
# df_json, dict1 = json_to_dataframe('path_to_json_file.json')

