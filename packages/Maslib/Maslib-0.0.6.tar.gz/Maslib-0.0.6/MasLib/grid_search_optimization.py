from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from catboost import CatBoostRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score

def grid_search_gb_boost(X, y, param_grid=None, cv=3, scoring='neg_mean_squared_error', cv_evaluate=10):
    if param_grid is None:
        param_grid = {
            'n_estimators': [100, 150, 200],
            'learning_rate': [0.1, 0.05, 0.01],
            'max_depth': [3, 4, 5]
        }
    model = GradientBoostingRegressor(random_state=42)
    return _grid_search_optimization(model, param_grid, X, y, cv, scoring, cv_evaluate)

def grid_search_rf(X, y, param_grid=None, cv=3, scoring='neg_mean_squared_error', cv_evaluate=10):
    if param_grid is None:
        param_grid = {
            'n_estimators': [100, 150, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
    model = RandomForestRegressor(random_state=42)
    return _grid_search_optimization(model, param_grid, X, y, cv, scoring, cv_evaluate)

def grid_search_lr(X, y, param_grid=None, cv=3, scoring='neg_mean_squared_error', cv_evaluate=10):
    if param_grid is None:
        param_grid = {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        }
    model = LinearRegression()
    return _grid_search_optimization(model, param_grid, X, y, cv, scoring, cv_evaluate)

def grid_search_catboost(X, y, param_grid=None, cv=3, scoring='neg_mean_squared_error', cv_evaluate=10):
    if param_grid is None:
        param_grid = {
            'iterations': [500, 1000],
            'depth': [4, 6, 8],
            'learning_rate': [0.1, 0.05, 0.01]
        }
    model = CatBoostRegressor(random_state=42, silent=True)
    return _grid_search_optimization(model, param_grid, X, y, cv, scoring, cv_evaluate)

def _grid_search_optimization(model, param_grid, X, y, cv, scoring, cv_evaluate):
    grid_search = GridSearchCV(model, param_grid, cv=cv, scoring=scoring)
    grid_search.fit(X, y)

    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    scores = cross_val_score(best_model, X, y, cv=cv_evaluate, scoring='r2')
    mean_accuracy = scores.mean()

    return best_params, best_model, mean_accuracy