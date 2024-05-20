import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF, TruncatedSVD
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(documents_df: pd.DataFrame, text_column: str, stop_words: list, max_df=0.95, min_df=2):
    """
    Преобразование текстов в векторное представление с использованием CountVectorizer.

    Parameters:
    documents_df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название столбца с текстами для векторизации.
    stop_words (list): Список стоп-слов для исключения из текстов.
    max_df (float): Максимальная доля документов для фильтрации слов.
    min_df (int): Минимальная частота документа для фильтрации слов.

    Returns:
    X (sparse matrix): Векторизированное представление текстов.
    vectorizer (CountVectorizer): Объект CountVectorizer.
    """
    vectorizer = CountVectorizer(stop_words=stop_words, max_df=max_df, min_df=min_df)
    X = vectorizer.fit_transform(documents_df[text_column])
    return X, vectorizer

def lda_model(documents_df: pd.DataFrame, text_column: str, stop_words: list, n_components=5, random_state=42):
    """
    Тематическое моделирование с использованием Latent Dirichlet Allocation (LDA).

    Parameters:
    documents_df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название столбца с текстами для векторизации.
    stop_words (list): Список стоп-слов для исключения из текстов.
    n_components (int): Количество тем.
    random_state (int): Параметр для воспроизводимости.

    Returns:
    None
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    lda = LatentDirichletAllocation(n_components=n_components, random_state=random_state)
    lda.fit(X)

    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(lda.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def nmf_model(documents_df: pd.DataFrame, text_column: str, stop_words: list, n_components=5, random_state=42):
    """
    Тематическое моделирование с использованием Non-Negative Matrix Factorization (NMF).

    Parameters:
    documents_df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название столбца с текстами для векторизации.
    stop_words (list): Список стоп-слов для исключения из текстов.
    n_components (int): Количество тем.
    random_state (int): Параметр для воспроизводимости.

    Returns:
    None
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    nmf = NMF(n_components=n_components, random_state=random_state)
    nmf.fit(X)

    for topic_idx, topic in enumerate(nmf.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(nmf.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def lsa_model(documents_df: pd.DataFrame, text_column: str, stop_words: list, n_components=5, random_state=42):
    """
    Тематическое моделирование с использованием Latent Semantic Analysis (LSA).

    Parameters:
    documents_df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название столбца с текстами для векторизации.
    stop_words (list): Список стоп-слов для исключения из текстов.
    n_components (int): Количество тем.
    random_state (int): Параметр для воспроизводимости.

    Returns:
    None
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    lsa = TruncatedSVD(n_components=n_components, random_state=random_state)
    lsa.fit(X)

    for topic_idx, topic in enumerate(lsa.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(lsa.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def tfidf_vectorize_texts(df, text_column, stop_words='english'):
    """
    Векторизация текстов с помощью TfidfVectorizer.

    Parameters:
    df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название колонки с текстом.
    stop_words (str or list): Список стоп-слов.

    Returns:
    tfidf_df (pd.DataFrame): DataFrame с TF-IDF векторами.
    """
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_vectors = vectorizer.fit_transform(df[text_column])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(tfidf_vectors.toarray(), columns=feature_names)
    return tfidf_df

def elbow_method_tfidf(df, text_column, stop_words='english', k_range=range(2, 11)):
    """
    Метод локтя для выбора оптимального количества кластеров с использованием TF-IDF.

    Parameters:
    df (pd.DataFrame): DataFrame с текстовыми данными.
    text_column (str): Название колонки с текстом.
    stop_words (str or list): Список стоп-слов.
    k_range (range): Диапазон количества кластеров.

    Returns:
    None
    """
    tfidf_df = tfidf_vectorize_texts(df, text_column, stop_words)
    scaler = StandardScaler()
    scaled_tfidf = scaler.fit_transform(tfidf_df)
    
    silhouette_scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans_labels = kmeans.fit_predict(scaled_tfidf)
        silhouette_score_avg = silhouette_score(scaled_tfidf, kmeans_labels)
        silhouette_scores.append(silhouette_score_avg)
    
    plt.plot(k_range, silhouette_scores, marker='o', linestyle='--', color='b')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xticks(k_range)
    plt.grid(True)
    plt.show()