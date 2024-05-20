import unittest
import numpy as np
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from MasLib.grid_search_optimization import grid_search_gb_boost, grid_search_rf, grid_search_lr, grid_search_catboost

class TestGridSearch(unittest.TestCase):

    def setUp(self):
        self.boston = load_boston()
        self.X = self.boston.data
        self.y = self.boston.target
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

    def test_grid_search_gb_boost(self):
        param_grid = {
            'n_estimators': [100, 150, 200],
            'learning_rate': [0.1, 0.05, 0.01],
            'max_depth': [3, 4, 5]
        }
        best_params, best_model, mean_accuracy = grid_search_gb_boost(self.X_train, self.y_train, param_grid=param_grid, cv=3, cv_evaluate=5)

        self.assertIsInstance(best_params, dict)
        self.assertIsInstance(best_model, GradientBoostingRegressor)
        self.assertIsInstance(mean_accuracy, float)

    def test_grid_search_rf(self):
        param_grid = {
            'n_estimators': [100, 150, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        best_params, best_model, mean_accuracy = grid_search_rf(self.X_train, self.y_train, param_grid=param_grid, cv=3, cv_evaluate=5)

        self.assertIsInstance(best_params, dict)
        self.assertIsInstance(best_model, RandomForestRegressor)
        self.assertIsInstance(mean_accuracy, float)

    def test_grid_search_lr(self):
        param_grid = {
            'fit_intercept': [True, False],
            'normalize': [True, False]
        }
        best_params, best_model, mean_accuracy = grid_search_lr(self.X_train, self.y_train, param_grid=param_grid, cv=3, cv_evaluate=5)

        self.assertIsInstance(best_params, dict)
        self.assertIsInstance(best_model, LinearRegression)
        self.assertIsInstance(mean_accuracy, float)

    def test_grid_search_catboost(self):
        param_grid = {
            'iterations': [500, 1000],
            'depth': [4, 6, 8],
            'learning_rate': [0.1, 0.05, 0.01]
        }
        best_params, best_model, mean_accuracy = grid_search_catboost(self.X_train, self.y_train, param_grid=param_grid, cv=3, cv_evaluate=5)

        self.assertIsInstance(best_params, dict)
        self.assertIsInstance(best_model, CatBoostRegressor)
        self.assertIsInstance(mean_accuracy, float)

if __name__ == '__main__':
    unittest.main()