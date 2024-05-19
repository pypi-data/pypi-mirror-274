import unittest
import pandas as pd
from MasLib.correlation import compute_phik_matrix, plot_phik_correlation_matrix

class TestCorrelation(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            'feature1': ['a', 'b', 'c', 'a', 'b'],
            'feature2': ['x', 'y', 'z', 'x', 'y'],
            'target': [1, 0, 1, 0, 1]
        })

    def test_compute_phik_matrix(self):
        encoded_data = self.sample_data.copy()
        encoded_data['feature1'] = encoded_data['feature1'].astype('category')
        encoded_data['feature2'] = encoded_data['feature2'].astype('category')

        phik_matrix = compute_phik_matrix(encoded_data)
        self.assertIsInstance(phik_matrix, pd.DataFrame)
        self.assertEqual(len(phik_matrix), len(encoded_data.columns))
        self.assertEqual(len(phik_matrix.columns), len(encoded_data.columns))

    def test_plot_phik_correlation_matrix(self):
        encoded_data = self.sample_data.copy()
        encoded_data['feature1'] = encoded_data['feature1'].astype('category')
        encoded_data['feature2'] = encoded_data['feature2'].astype('category')

        phik_matrix = compute_phik_matrix(encoded_data)

        # Проверяем, что график успешно отображается
        plot_phik_correlation_matrix(phik_matrix)

if __name__ == '__main__':
    unittest.main()
