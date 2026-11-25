import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
import sys

# Определяем папку проекта
BASE_DIR = Path(__file__).resolve().parent

# Путь к исходному Excel-файлу
DATA_PATH = BASE_DIR / "Data" / "Online Retail.xlsx"

# Папка для результатов
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

print("-" * 60)
print("Практическая работа: ONLiNE RETAiL")
print("-" * 60)

print("\nЭТАП 1. ЗАГРУЗКА ДАННЫХ")

# Проверяем наличие файла
if not DATA_PATH.exists():
    print("Файл Online Retail.xlsx не найден!")
    print("Поместите файл в папку Data.")
    sys.exit()

# Загружаем датасет
df = pd.read_excel(DATA_PATH)

print("\nДанные успешно загружены!")

# Размерность
print("\nРазмер датасета:")
print("Количество строк:", df.shape[0])
print("Количество столбцов:", df.shape[1])

# Первые строки
print("\nПервые 5 строк:")
print(df.head())

# Типы данных и заполненность
print("\nИнформация о датасете:")
df.info()

# Пропуски
print("\nКоличество пропусков:")
print(df.isna().sum())

# Дубликаты
print("\nКоличество дубликатов:")
print(df.duplicated().sum())

print("\nЭТАП 1 ЗАВЕРШЁН")