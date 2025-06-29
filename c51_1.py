import csv  # Работа с CSV-файлами
from datetime import datetime  # Работа с датой/временем
import pandas as pd  # Анализ данных
import matplotlib.pyplot as plt  # Визуализация данных
import os

WEATHER_LOG_PATH = "weather_logs.csv"
ADMIN_IDS = ["1512571026"]  # ID администраторов
# Создание файла логов при первом запуске
if not os.path.exists(WEATHER_LOG_PATH):
    with open(WEATHER_LOG_PATH, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'user_id', 'username', 'city', 'status'
        ])

def log_weather_request(user_id: int, username: str, city: str, status: str):
    with open(WEATHER_LOG_PATH, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),  # Текущее время
            user_id,
            username,
            city,
            status  # 'success', 'error' или 'city not found'
        ])

def weather_stats(update: Update, context: CallbackContext):
    # Чтение CSV в DataFrame
    df = pd.read_csv(WEATHER_LOG_PATH)
    total_requests = len(df)
    success_requests = df[df['status'] == 'success'].shape[0]
    unique_users = df['user_id'].nunique()
    # Топ городов
    popular_cities = df[df['status'] == 'success']['city'].value_counts().head(5)
    # Анализ по времени
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_activity = df.groupby('date').size()

