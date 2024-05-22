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

def tfidf_vectorization(df, column_name, stop_words):
    # Создаем векторизатор TF-IDF
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    # Преобразуем текст в TF-IDF матрицу
    tfidf_matrix = vectorizer.fit_transform(df[column_name])
    # Получаем имена признаков
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    # Сортируем ключевые слова по их весу TF-IDF
    sorted_features = sorted(zip(tfidf_scores, feature_names), reverse=True)
    
    # Выводим топ-10 ключевых слов/биграмм/триграмм
    for score, feature in sorted_features[:10]:
        print(f"{feature}: {score:.3f}")
    
    # Преобразуем TF-IDF матрицу в DataFrame и добавляем к исходному DataFrame
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
    df_vec = pd.concat([df, tfidf_df], axis=1)
    return df_vec

def bert_topic_modeling(texts):
    # Создаем модель тематического моделирования BERTopic
    topic_model = BERTopic(language="russian", calculate_probabilities=True, verbose=True, embedding_model='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', n_gram_range=(2, 2))
    topics, probs = topic_model.fit_transform(texts)
    topic_model.visualize_barchart()
    return topics, probs

def lda_topic_modeling(df, column_name, stop_words):
    # Создаем TF-IDF векторизатор
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.9, min_df=0.2)
    # Преобразуем текст в TF-IDF матрицу
    data_text_modeling = vectorizer.fit_transform(df[column_name])
    
    # Создаем модель LDA
    lda = LatentDirichletAllocation(n_components=10, random_state=42)
    lda.fit(data_text_modeling)
    
    # Применяем TSNE для визуализации
    tsne_model = TSNE(n_components=2, init='random')
    tsne_results = tsne_model.fit_transform(data_text_modeling)
    
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1])
    plt.show()
    
    # Выводим топики
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Топик {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()
    
    # Визуализируем облако слов для каждого топика
    for topic_idx, topic in enumerate(lda.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Облако слов для топика {topic_idx + 1}')
        plt.axis('off')
        plt.show()

# Пример использования:
# df = pd.read_csv('path_to_csv')
# tfidf_vectorization(df, 'text_column', ['stop', 'words'])
# bert_topic_modeling(df['text_column'].tolist())
# lda_topic_modeling(df, 'text_column', ['stop', 'words'])