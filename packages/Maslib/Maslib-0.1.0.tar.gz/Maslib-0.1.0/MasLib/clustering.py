import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

def scale_data(X):
    """
    Масштабирование данных.

    Parameters:
    X (np.ndarray): Массив данных.

    Returns:
    X_scaled (np.ndarray): Масштабированный массив данных.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled

def kmeans_clustering(X, n_clusters=4, random_state=0):
    """
    Кластеризация с помощью K-means.

    Parameters:
    X (np.ndarray): Массив данных.
    n_clusters (int): Количество кластеров.
    random_state (int): Параметр для воспроизводимости.

    Returns:
    labels (np.ndarray): Массив меток кластеров.
    silhouette (float): Значение метрики силуэт.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    return labels, silhouette

def hierarchical_clustering(X, n_clusters=4):
    """
    Иерархическая кластеризация.

    Parameters:
    X (np.ndarray): Массив данных.
    n_clusters (int): Количество кластеров.

    Returns:
    labels (np.ndarray): Массив меток кластеров.
    silhouette (float): Значение метрики силуэт.
    """
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hierarchical.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    return labels, silhouette

def dbscan_clustering(X, eps=0.3, min_samples=10):
    """
    Кластеризация с помощью DBSCAN.

    Parameters:
    X (np.ndarray): Массив данных.
    eps (float): Максимальное расстояние между двумя образцами для их объединения в один кластер.
    min_samples (int): Минимальное количество образцов в кластере.

    Returns:
    labels (np.ndarray): Массив меток кластеров.
    silhouette (float): Значение метрики силуэт.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X)
    silhouette = silhouette_score(X, labels)
    return labels, silhouette

def calculate_metrics(X, labels):
    """
    Расчет метрик кластеризации.

    Parameters:
    X (np.ndarray): Массив данных.
    labels (np.ndarray): Массив меток кластеров.

    Returns:
    metrics (dict): Словарь с метриками кластеризации.
    """
    silhouette = silhouette_score(X, labels)
    calinski_harabasz = calinski_harabasz_score(X, labels)
    davies_bouldin = davies_bouldin_score(X, labels)
    
    metrics = {
        'silhouette': silhouette,
        'calinski_harabasz': calinski_harabasz,
        'davies_bouldin': davies_bouldin
    }
    return metrics

def visualize_clustering(X, labels_list, titles):
    """
    Визуализация результатов кластеризации.

    Parameters:
    X (np.ndarray): Массив данных.
    labels_list (list of np.ndarray): Список массивов меток кластеров.
    Пример: labels_list = [kmeans_labels, hierarchical_labels, dbscan_labels]
    titles (list of str): Список заголовков для каждого графика.
    """
    plt.figure(figsize=(18, 6))
    for i, (labels, title) in enumerate(zip(labels_list, titles)):
        plt.subplot(1, len(labels_list), i+1)
        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
        plt.title(title)
    plt.show()