import unittest
import pandas as pd
from sklearn import preprocessing
from MasLib.encoding import number_encode_features

class TestEncoding(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            'feature1': ['a', 'b', 'c', 'a', 'b'],
            'feature2': ['x', 'y', 'z', 'x', 'y'],
            'target': [1, 0, 1, 0, 1]
        })

    def test_number_encode_features(self):
        encoded_data, encoders = number_encode_features(self.sample_data)
        self.assertIsInstance(encoded_data, pd.DataFrame)
        self.assertIn('feature1', encoded_data.columns)
        self.assertIn('feature2', encoded_data.columns)
        self.assertIn('target', encoded_data.columns)

        # Проверяем, что категориальные признаки были успешно закодированы
        self.assertTrue(all(isinstance(value, int) for value in encoded_data['feature1']))
        self.assertTrue(all(isinstance(value, int) for value in encoded_data['feature2']))

        # Проверяем, что кодировщики были созданы и использованы
        self.assertIn('feature1', encoders)
        self.assertIn('feature2', encoders)
        self.assertIsInstance(encoders['feature1'], preprocessing.LabelEncoder)
        self.assertIsInstance(encoders['feature2'], preprocessing.LabelEncoder)

if __name__ == '__main__':
    unittest.main()

