from sentence_transformers import SentenceTransformer
import pandas as pd
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from Get_dictionary_Michael import Get_DF_from_Dictionary, Get_Small_Dictionary_from_Excel
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import os
#Используем мультиангл из практического занятия

#класс для эмбеддинга
class TextDatabase:
    def __init__(self, db_path='RAG_seminar2.db', model_name='intfloat/multilingual-e5-base'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.model = SentenceTransformer(model_name)

    def find_nearest_text(self, text, k=5):
        task_vector = self.model.encode([text])[0]
        
        # Извлечение эмбеддингов из бд
        self.cursor.execute("SELECT Text, embeddings FROM texts")
        rows = self.cursor.fetchall()

        # Декодирование эмбеддингов и поиск косинусного расстояния
        embeddings = np.array([np.frombuffer(row[1], dtype=np.float32) for row in rows])
        similarities = cosine_similarity([task_vector], embeddings)[0]

        # найти индексы k ближайших
        nearest_indices = similarities.argsort()[-k:][::-1]

        # вернуть k ближайших
        nearest_text = [rows[i] for i in nearest_indices]
        return nearest_text

    def close(self):
        self.conn.close()
  
#функция загрузки файлов 
def select_excel_files():
    # Создаем корневое окно и скрываем его
    root = tk.Tk()
    root.withdraw()

    # Разрешаем пользователю выбрать несколько файлов
    file_paths = filedialog.askopenfilenames(
        title="Выберите файлы Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    # Преобразуем выбранные пути в список строк с префиксом r
    filePathList = [rf'{Path(path)}' for path in file_paths]
        
    # Преобразуем пути в формат списка
    file_path_list = list(file_paths)

    return file_path_list

#получаем ближайшие слова для одного датафрейма, n ближайших значений, request- запрос
def get_words_from_multilingual_e5_base(test_texts, n, request):
    # Проверяем существование файла перед удалением (опционально)
    file_path = 'RAG_seminar2.db'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    else:
        print(f"Файл {file_path} не существует.")
    conn = sqlite3.connect('RAG_seminar2.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS texts
                (Text TEXT, embeddings BLOB)''')
    conn.commit()
    model = SentenceTransformer('intfloat/multilingual-e5-base')
    task_vectors = model.encode(
        test_texts.apply(
            lambda row: f"{row['text']}",
            axis=1
        ).tolist(),
        normalize_embeddings=True
    )

    task_vectors_bytes = [vector.tobytes() for vector in task_vectors]

    for i, row in test_texts.iterrows():
        cursor.execute(
            '''INSERT INTO texts (Text, embeddings)
            VALUES (?,  ?)''',
            (row['text'], task_vectors_bytes[i])
        )
    conn.commit()
    conn.close()
    
   
    td = TextDatabase(db_path='RAG_seminar2.db')
    a = td.find_nearest_text(text=request,k=n)
    return a

#Пример использования
#In[]
#выбираем файлы
path=select_excel_files()
print(path)
#получаем словарь с заголовками
s=Get_Small_Dictionary_from_Excel(path)
#получаем датафрейм из словаря
test_texts=Get_DF_from_Dictionary(s)
print(test_texts)
#получаем ответ в виле списка заголовков [list]
answer= get_words_from_multilingual_e5_base(test_texts,3,'скважина') 
new_list = [item[0] for item in answer]
print(new_list)