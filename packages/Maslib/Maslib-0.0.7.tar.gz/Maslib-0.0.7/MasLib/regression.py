from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import cross_val_score
import numpy as np

def gb_regression(X_train, X_test, y_train, y_test):
    """
    Функция для тренировки и оценки модели CatBoostRegression.

    Parameters:
    X_train: обучающая выборка признаков
    X_test: тестовая выборка признаков
    y_train: обучающая выборка целевой переменной
    y_test: тестовая выборка целевой переменной

    Returns:
    dict: Словарь с оценками модели (MAE, MSE, RMSE, R^2)
    """
    gb_model = GradientBoostingRegressor(random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred = gb_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': gb_model.score(X_test, y_test)
    }
    
    return results, gb_model

def rf_regression(X_train, X_test, y_train, y_test):
    """
    Функция для тренировки и оценки модели CatBoostRegression.

    Parameters:
    X_train: обучающая выборка признаков
    X_test: тестовая выборка признаков
    y_train: обучающая выборка целевой переменной
    y_test: тестовая выборка целевой переменной

    Returns:
    dict: Словарь с оценками модели (MAE, MSE, RMSE, R^2)
    """
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': rf_model.score(X_test, y_test)
    }
    
    return results, rf_model

def lr_regression(X_train, X_test, y_train, y_test):
    """
    Функция для тренировки и оценки модели CatBoostRegression.

    Parameters:
    X_train: обучающая выборка признаков
    X_test: тестовая выборка признаков
    y_train: обучающая выборка целевой переменной
    y_test: тестовая выборка целевой переменной

    Returns:
    dict: Словарь с оценками модели (MAE, MSE, RMSE, R^2)
    """
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred = lr_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': lr_model.score(X_test, y_test)
    }
    
    return results, lr_model

def catboost_regression(X_train, X_test, y_train, y_test):
    """
    Функция для тренировки и оценки модели CatBoostRegression.

    Parameters:
    X_train: обучающая выборка признаков
    X_test: тестовая выборка признаков
    y_train: обучающая выборка целевой переменной
    y_test: тестовая выборка целевой переменной

    Returns:
    dict: Словарь с оценками модели (MAE, MSE, RMSE, R^2)
    """
    catboost_model = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, loss_function='RMSE', random_state=42)
    catboost_model.fit(X_train, y_train, verbose=100)
    y_pred = catboost_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    results = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': catboost_model.score(X_test, y_test)
    }
    
    return results, catboost_model

def cross_val_evaluate(model, X, y, cv=5, scoring='neg_mean_squared_error'):
    """
    Функция для Кросс валидации модели.

    Parameters:
    model: Модель регресии
    X_test: тестовая выборка признаков
    y_test: тестовая выборка целевой переменной

    Returns:
    dict: Словарь с оценками модели (RMSE per fold, Mean RMSE)
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    rmse_scores = np.sqrt(-scores)
    
    model.fit(X, y)
    
    results = {
        'RMSE per fold': rmse_scores,
        'Mean RMSE': rmse_scores.mean()
    }
    
    return results, model
