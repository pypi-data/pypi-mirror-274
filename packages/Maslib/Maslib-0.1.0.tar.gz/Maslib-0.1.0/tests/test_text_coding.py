import unittest
import pandas as pd
import numpy as np
from your_module import vectorize_text, lda_model, nmf_model, lsa_model, tfidf_vectorize_texts, elbow_method_tfidf

class TestTextAnalysis(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'text': ['This is a sample text.', 'Another sample text for testing.', 'Yet another text for testing.'],
            'label': [1, 0, 1]
        })

    def test_vectorize_text(self):
        X, vectorizer = vectorize_text(self.data, 'text', stop_words='english')
        self.assertIsInstance(X, (np.ndarray, np.matrix))
        self.assertIsInstance(vectorizer, CountVectorizer)

    def test_lda_model(self):
        lda_model(self.data, 'text', stop_words='english', n_components=3)

    def test_nmf_model(self):
        nmf_model(self.data, 'text', stop_words='english', n_components=3)

    def test_lsa_model(self):
        lsa_model(self.data, 'text', stop_words='english', n_components=3)

    def test_tfidf_vectorize_texts(self):
        tfidf_df = tfidf_vectorize_texts(self.data, 'text', stop_words='english')
        self.assertIsInstance(tfidf_df, pd.DataFrame)
        self.assertEqual(tfidf_df.shape[0], self.data.shape[0])

    def test_elbow_method_tfidf(self):
        elbow_method_tfidf(self.data, 'text', stop_words='english', k_range=range(2, 6))

if __name__ == '__main__':
    unittest.main()
