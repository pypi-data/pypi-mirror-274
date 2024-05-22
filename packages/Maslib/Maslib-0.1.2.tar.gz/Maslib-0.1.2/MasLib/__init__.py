from .encoding import number_encode_features, process_column_and_merge,json_to_dataframe
from .correlation import compute_phik_matrix, plot_phik_correlation_matrix
from .regressions import gb_regression, rf_regression, lr_regression, catboost_regression, cross_val_evaluate
from .grid_search_optimization import grid_search_gb_boost, grid_search_rf, grid_search_lr, grid_search_catboost
from .loading import save_model
from .text_coding import vectorize_text, lda_model, nmf_model, lsa_model, tfidf_vectorize_texts, elbow_method_tfidf, tfidf_vectorization, bert_topic_modeling, lda_topic_modeling
from .clustering import scale_data, kmeans_clustering, hierarchical_clustering, dbscan_clustering, calculate_metrics, visualize_clustering
from .classification import classification_with_svc, classification_with_random_forest, classification_with_knn