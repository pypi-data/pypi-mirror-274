import unittest
import joblib
import os
from your_module import save_model

class TestSaveModel(unittest.TestCase):

    def setUp(self):
        self.model = "test_model.pkl"

    def test_save_model(self):
        save_model(self.model, file_path='test_model.pkl')
        self.assertTrue(os.path.exists('test_model.pkl'))
        os.remove('test_model.pkl')

if __name__ == '__main__':
    unittest.main()