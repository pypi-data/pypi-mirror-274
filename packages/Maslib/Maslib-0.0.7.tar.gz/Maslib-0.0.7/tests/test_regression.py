import unittest
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.ensemble import GradientBoostingRegressor
from MasLib.regression import gb_boost_regression, rf_regression, lr_regression, catboost_regression, cross_val_evaluate

class TestRegression(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        boston = load_boston()
        X = boston.data
        y = boston.target
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def test_gb_boost_regression(self):
        results, model = gb_boost_regression(self.X_train, self.X_test, self.y_train, self.y_test)
        self.assertIn('MAE', results)
        self.assertIn('MSE', results)
        self.assertIn('RMSE', results)
        self.assertIn('R2', results)
        self.assertIsNotNone(model)

    def test_rf_regression(self):
        results, model = rf_regression(self.X_train, self.X_test, self.y_train, self.y_test)
        self.assertIn('MAE', results)
        self.assertIn('MSE', results)
        self.assertIn('RMSE', results)
        self.assertIn('R2', results)
        self.assertIsNotNone(model)

    def test_lr_regression(self):
        results, model = lr_regression(self.X_train, self.X_test, self.y_train, self.y_test)
        self.assertIn('MAE', results)
        self.assertIn('MSE', results)
        self.assertIn('RMSE', results)
        self.assertIn('R2', results)
        self.assertIsNotNone(model)

    def test_catboost_regression(self):
        results, model = catboost_regression(self.X_train, self.X_test, self.y_train, self.y_test)
        self.assertIn('MAE', results)
        self.assertIn('MSE', results)
        self.assertIn('RMSE', results)
        self.assertIn('R2', results)
        self.assertIsNotNone(model)
        
    def test_cross_val_evaluate(self):
        model = GradientBoostingRegressor(random_state=42)
        results, trained_model = cross_val_evaluate(model, self.X_train, self.y_train, cv=5, scoring='neg_mean_squared_error')
        self.assertIn('RMSE per fold', results)
        self.assertIn('Mean RMSE', results)
        self.assertIsNotNone(trained_model)

if __name__ == '__main__':
    unittest.main()
