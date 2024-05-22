import unittest
import pandas as pd
import numpy as np
from your_module import scale_data, kmeans_clustering, hierarchical_clustering, dbscan_clustering, calculate_metrics, visualize_clustering

class TestClustering(unittest.TestCase):

    def setUp(self):
        self.data = np.random.rand(100, 2)

    def test_scale_data(self):
        scaled_data = scale_data(self.data)
        self.assertTrue(np.allclose(np.mean(scaled_data, axis=0), 0))
        self.assertTrue(np.allclose(np.std(scaled_data, axis=0), 1))

    def test_kmeans_clustering(self):
        labels, silhouette = kmeans_clustering(self.data, n_clusters=3)
        self.assertEqual(len(labels), len(self.data))
        self.assertIsInstance(silhouette, float)

    def test_hierarchical_clustering(self):
        labels, silhouette = hierarchical_clustering(self.data, n_clusters=3)
        self.assertEqual(len(labels), len(self.data))
        self.assertIsInstance(silhouette, float)

    def test_dbscan_clustering(self):
        labels, silhouette = dbscan_clustering(self.data, eps=0.5, min_samples=5)
        self.assertEqual(len(labels), len(self.data))
        self.assertIsInstance(silhouette, float)

    def test_calculate_metrics(self):
        labels = np.random.randint(0, 3, size=100)
        metrics = calculate_metrics(self.data, labels)
        self.assertIsInstance(metrics, dict)
        self.assertIn('silhouette', metrics)
        self.assertIn('calinski_harabasz', metrics)
        self.assertIn('davies_bouldin', metrics)

if __name__ == '__main__':
    unittest.main()
