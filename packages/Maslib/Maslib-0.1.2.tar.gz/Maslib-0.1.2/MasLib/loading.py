import joblib

def save_model(model, file_path='best_model.pkl'):
    """
    Функция для сохранения модели в файл.

    Parameters:
    model: Модель, которую необходимо сохранить.
    file_path (str): Путь к файлу, в который будет сохранена модель.
    """
    joblib.dump(model, file_path)
    print(f"Модель сохранена в {file_path}")