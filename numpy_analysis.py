
from pathlib import Path

import pandas as pd
import numpy as np

# ----------------------------------------------------------
# ЭТАП 21. СТАТИСТИЧЕСКИЙ АНАЛИЗ И ПРЕОБРАЗОВАНИЕ NUMPY
# ----------------------------------------------------------

print("\n" + "-" * 65)
print("ЭТАП 21. Статистический анализ и преобразование NUMPY")
print("-" * 65)

# 1. Пути к файлам
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

DATA_PATH = RESULTS_DIR / "Online_Retail_sales.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Файл не найден: {DATA_PATH}")

# 2. Загрузка данных
df = pd.read_csv(DATA_PATH)

print("\n1. Загрузка данных")
print("Размер исходной таблицы:", df.shape)

# 3. Выбираем числовые признаки
features = ["Quantity", "UnitPrice", "Revenue"]

missing_columns = [col for col in features if col not in df.columns]

if missing_columns:
    raise ValueError(f"Отсутствуют столбцы: {missing_columns}")

# Преобразуем признаки в числовой формат
numeric_df = df[features].apply(
    pd.to_numeric,
    errors="coerce"
)

# Создаём массив NumPy
X = numeric_df.to_numpy(dtype=np.float64)

print("\n2. Информация о массиве NUMPY")
print("Размер массива:", X.shape)
print("Количество строк:", X.shape[0])
print("Количество признаков:", X.shape[1])
print("Тип данных:", X.dtype)
print("Объём памяти, байт:", X.nbytes)
print("Объём памяти, МБ:", round(X.nbytes / (1024 ** 2), 2))

# 4. Анализ качества числовых признаков
print("\n3. Анализ качества данных")

missing_counts = np.isnan(X).sum(axis=0)
positive_counts = (X > 0).sum(axis=0)
negative_counts = (X < 0).sum(axis=0)
zero_counts = (X == 0).sum(axis=0)

quality_report = pd.DataFrame({
    "Feature": features,
    "Missing": missing_counts,
    "Positive": positive_counts,
    "Negative": negative_counts,
    "Zero": zero_counts
})

print(quality_report.to_string(index=False))

# Для дальнейших расчётов используем строки без пропусков
valid_mask = np.isfinite(X).all(axis=1)
X_valid = X[valid_mask]

if len(X_valid) == 0:
    raise ValueError("Нет строк без пропущенных или бесконечных значений.")

print("\nСтрок для статистического анализа:", len(X_valid))
print("Исключено строк с некорректными значениями:", len(X) - len(X_valid))

# 5. Статистический анализ
print("\n4. Статистический анализ")

statistics = []

for i, feature in enumerate(features):
    values = X_valid[:, i]

    statistics.append({
        "Feature": feature,
        "Mean": np.mean(values),
        "Median": np.median(values),
        "Minimum": np.min(values),
        "Maximum": np.max(values),
        "Variance": np.var(values),
        "Std": np.std(values),
        "Q1": np.quantile(values, 0.25),
        "Q2": np.quantile(values, 0.50),
        "Q3": np.quantile(values, 0.75),
        "IQR": (
            np.quantile(values, 0.75)
            - np.quantile(values, 0.25)
        )
    })

statistics_df = pd.DataFrame(statistics)

print(statistics_df.round(4).to_string(index=False))

statistics_df.to_csv(
    RESULTS_DIR / "NumPy_Statistics.csv",
    index=False,
    encoding="utf-8-sig"
)

# 6. Z-score стандартизация
print("\n5. Z-SCORE стандартизация")

mean_values = np.mean(X_valid, axis=0)
std_values = np.std(X_valid, axis=0)

# Защита от деления на ноль
safe_std = np.where(std_values == 0, 1, std_values)

Z = (X_valid - mean_values) / safe_std

print("Средние значения после стандартизации:")
print(np.mean(Z, axis=0).round(6))

print("Стандартные отклонения после стандартизации:")
print(np.std(Z, axis=0).round(6))

# 7. Robust Z-score и Modified Z-score
print("\n6. ROBUST Z-SCORE И MODIFIED Z-SCORE")

medians = np.median(X_valid, axis=0)

mad = np.median(
    np.abs(X_valid - medians),
    axis=0
)

safe_mad = np.where(mad == 0, 1, mad)

robust_Z = (X_valid - medians) / safe_mad

modified_Z = 0.6745 * robust_Z

# Потенциальные выбросы по Modified Z-score
modified_outliers = np.abs(modified_Z) > 3.5

print("Количество потенциальных выбросов по признакам:")
for i, feature in enumerate(features):
    print(
        feature,
        ":",
        int(modified_outliers[:, i].sum())
    )

# 8. Mean Normalization
print("\n7. MEAN NORMALIZATION")

min_values = np.min(X_valid, axis=0)
max_values = np.max(X_valid, axis=0)

safe_ranges = np.where(
    max_values - min_values == 0,
    1,
    max_values - min_values
)

mean_normalized = (
    X_valid - mean_values
) / safe_ranges

print(
    "Минимальные значения:",
    mean_normalized.min(axis=0).round(4)
)
print(
    "Максимальные значения:",
    mean_normalized.max(axis=0).round(4)
)

# 9. Unit Variance Scaling
print("\n8. UNIT VARIANCE SCALING")

unit_variance = (
    X_valid - mean_values
) / safe_std

print("Дисперсия преобразованных признаков:")
print(np.var(unit_variance, axis=0).round(6))

# 10. L1-нормализация
print("\n9. L1-нормализация")

l1_denominator = np.sum(
    np.abs(X_valid),
    axis=1,
    keepdims=True
)

l1_denominator = np.where(
    l1_denominator == 0,
    1,
    l1_denominator
)

l1_normalized = X_valid / l1_denominator

print(
    "Первые 3 строки L1-нормализации:"
)
print(l1_normalized[:3].round(6))

# 11. L2-нормализация
print("\n10. L2-нормализация")

l2_denominator = np.sqrt(
    np.sum(X_valid ** 2, axis=1, keepdims=True)
)

l2_denominator = np.where(
    l2_denominator == 0,
    1,
    l2_denominator
)

l2_normalized = X_valid / l2_denominator

print(
    "Первые 3 строки L2-нормализации:"
)
print(l2_normalized[:3].round(6))

# 12. Max-нормализация
print("\n11. MAX-нормализация")

safe_max = np.where(max_values == 0, 1, max_values)

max_normalized = X_valid / safe_max

print(
    "Максимумы после нормализации:"
)
print(max_normalized.max(axis=0).round(6))

# 13. Probability Normalization
print("\n12. PROBABILITY NORMALIZATION")

# Преобразование выполняется отдельно по каждому признаку.
# Для вероятностной интерпретации используем только
# неотрицательные значения.
if np.any(X_valid < 0):
    raise ValueError(
        "Для Probability Normalization обнаружены отрицательные значения."
    )

column_sums = np.sum(X_valid, axis=0)

safe_sums = np.where(column_sums == 0, 1, column_sums)

probability_normalized = X_valid / safe_sums

print("Сумма значений по признакам:")
print(probability_normalized.sum(axis=0).round(6))

# 14. Формирование таблицы преобразованных данных
transformed_df = pd.DataFrame({
    "Quantity_Zscore": Z[:, 0],
    "UnitPrice_Zscore": Z[:, 1],
    "Revenue_Zscore": Z[:, 2],

    "Quantity_RobustZ": robust_Z[:, 0],
    "UnitPrice_RobustZ": robust_Z[:, 1],
    "Revenue_RobustZ": robust_Z[:, 2],

    "Quantity_ModifiedZ": modified_Z[:, 0],
    "UnitPrice_ModifiedZ": modified_Z[:, 1],
    "Revenue_ModifiedZ": modified_Z[:, 2],

    "Quantity_MeanNorm": mean_normalized[:, 0],
    "UnitPrice_MeanNorm": mean_normalized[:, 1],
    "Revenue_MeanNorm": mean_normalized[:, 2],

    "Quantity_UnitVariance": unit_variance[:, 0],
    "UnitPrice_UnitVariance": unit_variance[:, 1],
    "Revenue_UnitVariance": unit_variance[:, 2],

    "Quantity_L1": l1_normalized[:, 0],
    "UnitPrice_L1": l1_normalized[:, 1],
    "Revenue_L1": l1_normalized[:, 2],

    "Quantity_L2": l2_normalized[:, 0],
    "UnitPrice_L2": l2_normalized[:, 1],
    "Revenue_L2": l2_normalized[:, 2],

    "Quantity_MaxNorm": max_normalized[:, 0],
    "UnitPrice_MaxNorm": max_normalized[:, 1],
    "Revenue_MaxNorm": max_normalized[:, 2],

    "Quantity_Probability": probability_normalized[:, 0],
    "UnitPrice_Probability": probability_normalized[:, 1],
    "Revenue_Probability": probability_normalized[:, 2],

    "Quantity_Outlier": modified_outliers[:, 0],
    "UnitPrice_Outlier": modified_outliers[:, 1],
    "Revenue_Outlier": modified_outliers[:, 2]
})

# Сохраняем преобразованные значения
transformed_df.to_csv(
    RESULTS_DIR / "NumPy_Transformed_Data.csv",
    index=False,
    encoding="utf-8-sig"
)

# 15. Информационный отчёт
print("\n13. Информационный отчет")

information_report = pd.DataFrame({
    "Parameter": [
        "Исходное количество строк",
        "Количество строк для анализа",
        "Количество признаков",
        "Тип массива",
        "Размер массива NumPy",
        "Объём массива в МБ",
        "Количество пропусков",
        "Количество строк с некорректными значениями"
    ],
    "Value": [
        X.shape[0],
        X_valid.shape[0],
        X_valid.shape[1],
        str(X_valid.dtype),
        str(X_valid.shape),
        round(X_valid.nbytes / (1024 ** 2), 2),
        int(np.isnan(X).sum()),
        int((~valid_mask).sum())
    ]
})

print(information_report.to_string(index=False))

# 16. Сохраняем отчёты
quality_report.to_csv(
    RESULTS_DIR / "NumPy_Data_Quality.csv",
    index=False,
    encoding="utf-8-sig"
)

information_report.to_csv(
    RESULTS_DIR / "NumPy_Information_Report.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "-" * 65)
print("ЭТАП 21. NUMPY-АНАЛИЗ ЗАВЕРШЁН")
print("Все результаты сохранены в папке results.")
print("-" * 65)
