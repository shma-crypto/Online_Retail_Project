import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Data" / "Online Retail.xlsx"

df = pd.read_excel(DATA_PATH)

print("-" * 60)
print("ЭТАП 3. Детальная проверка аномалий")
print("-" * 60)

# Создаём признаки
df["IsCancelled"] = df["InvoiceNo"].astype(str).str.startswith("C")
df["IsNegativeQuantity"] = df["Quantity"] < 0
df["IsZeroPrice"] = df["UnitPrice"] == 0
df["IsNegativePrice"] = df["UnitPrice"] < 0

# 1. Проверяем пересечение отмен и отрицательного количества
print("\n1. Отменённые операции и отрицательное количество:")

print(pd.crosstab(
    df["IsCancelled"],
    df["IsNegativeQuantity"],
    rownames=["Отменённая операция"],
    colnames=["Отрицательное количество"]
))

# 2. Отрицательное количество без признака отмены
negative_without_cancel = df[
    (df["Quantity"] < 0) & (~df["IsCancelled"])
]

print("\n2. Отрицательное количество без C в InvoiceNo:")
print("Количество:", len(negative_without_cancel))
print(negative_without_cancel[
    ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
].head(10))

# 3. Примеры отменённых операций
cancelled_examples = df[df["IsCancelled"]]

print("\n3. Примеры отменённых операций:")
print(cancelled_examples[
    ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
].head(10))

# 4. Примеры товаров с нулевой ценой
zero_price_examples = df[df["UnitPrice"] == 0]

print("\n4. Примеры товаров с нулевой ценой:")
print(zero_price_examples[
    ["InvoiceNo", "StockCode", "Description", "Quantity", "Country"]
].head(10))

# 5. Отрицательные цены
negative_price_examples = df[df["UnitPrice"] < 0]

print("\n5. Записи с отрицательной ценой:")
print(negative_price_examples[
    ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
])

print("\nЭТАП 3 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 4. Проверка связей между аномалиями")
print("-" * 60)

# Выделяем отрицательное количество без отмены
negative_regular = df[
    (df["Quantity"] < 0) &
    (~df["IsCancelled"])
].copy()

print("\n1. Проверка 1336 отрицательных операций без отмены")

print("Всего записей:", len(negative_regular))

print("С нулевой ценой:",
      (negative_regular["UnitPrice"] == 0).sum())

print("С отсутствующим описанием:",
      negative_regular["Description"].isna().sum())

print("С отсутствующим CustomerID:",
      negative_regular["CustomerID"].isna().sum())

# Проверяем пересечение признаков
print("\n2. Совместное наличие признаков")

print(
    "Одновременно нулевая цена и отсутствующее описание:",
    (
        (negative_regular["UnitPrice"] == 0) &
        (negative_regular["Description"].isna())
    ).sum()
)

# Анализ нулевых цен
print("\n3. Анализ записей с нулевой ценой")

zero_price = df[df["UnitPrice"] == 0]

print("Всего записей:", len(zero_price))
print("Без описания:", zero_price["Description"].isna().sum())
print("С CustomerID:", zero_price["CustomerID"].notna().sum())
print("Без CustomerID:", zero_price["CustomerID"].isna().sum())

# Анализ специальных корректировок
print("\n4. Проверка корректировок задолженности")

adjustments = df[
    df["Description"].astype("string").str.contains(
        "Adjust bad debt",
        case=False,
        na=False
    )
]

print(adjustments)

print("\nПРОВЕРКА ЗАВЕРШЕНА")

print("\n" + "-" * 60)
print("ЭТАП 5. Проверка дубликатов")
print("-" * 60)

# Выделяем полные дубликаты
duplicates = df[df.duplicated(keep=False)]

print("\nКоличество строк, участвующих в повторах:")
print(len(duplicates))

print("\nКоличество повторных копий:")
print(df.duplicated().sum())

print("\nПервые 15 повторяющихся строк:")
print(duplicates.head(15).to_string(index=False))

# Проверяем дубликаты по ключевым полям
print("\nКоличество повторов по InvoiceNo и StockCode:")

print(
    df.duplicated(
        subset=["InvoiceNo", "StockCode"]
    ).sum()
)

print("\nЭТАП 5 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 6. Проверка повторных товарных позиций")
print("-" * 60)

# Группируем записи по заказу и товару
grouped = df.groupby(
    ["InvoiceNo", "StockCode"],
    dropna=False
)

# Считаем количество строк в каждой группе
group_sizes = grouped.size()

# Группы, где есть повторения
repeated_groups = group_sizes[group_sizes > 1]

print("\nКоличество групп с повторениями:")
print(len(repeated_groups))

print("\nКоличество строк в этих группах:")
print(repeated_groups.sum())

# Проверяем различия в количестве и цене
quantity_variations = grouped["Quantity"].nunique()
price_variations = grouped["UnitPrice"].nunique()

print("\nГруппы с различным количеством:")
print(
    ((group_sizes > 1) & (quantity_variations > 1)).sum()
)

print("\nГруппы с различной ценой:")
print(
    ((group_sizes > 1) & (price_variations > 1)).sum()
)

# Выводим примеры повторных позиций
print("\nПримеры повторных товарных позиций:")

examples = (
    df[df.duplicated(
        subset=["InvoiceNo", "StockCode"],
        keep=False
    )]
    .sort_values(["InvoiceNo", "StockCode"])
    .head(20)
)

print(examples[
    ["InvoiceNo", "StockCode", "Description",
     "Quantity", "UnitPrice"]
].to_string(index=False))

print("\nЭТАП 6 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 7. Удаление полных дубликатов")
print("-" * 60)

# Количество строк до удаления дубликатов
rows_before = len(df)

# Создаём отдельную таблицу без полных дубликатов
df_clean = df.drop_duplicates().copy()

# Количество строк после удаления
rows_after = len(df_clean)

# Сколько строк удалено
removed_rows = rows_before - rows_after

# Доля удалённых строк
removed_percent = removed_rows / rows_before * 100

print("Строк до удаления:", rows_before)
print("Строк после удаления:", rows_after)
print("Удалено полных дубликатов:", removed_rows)
print(f"Доля удалённых строк: {removed_percent:.2f}%")

# Проверяем, остались ли полные дубликаты
print("Оставшиеся полные дубликаты:", df_clean.duplicated().sum())

# Сохраняем результат
from pathlib import Path

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

df_clean.to_csv(
    RESULTS_DIR / "Online_Retail_without_exact_duplicates.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nОчищенная таблица сохранена в папке results.")
print("ЭТАП 7 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 8. Анализ пропущенных значений")
print("-" * 60)

# 1. Проверяем пропуски после удаления полных дубликатов
print("\n1. Количество пропусков по столбцам:")
print(df_clean.isnull().sum())

print("\n2. Доля пропусков по столбцам (%):")
print((df_clean.isnull().mean() * 100).round(2))

# 2. Проверяем, можно ли восстановить Description по StockCode
description_by_code = (
    df_clean.dropna(subset=["Description"])
    .groupby("StockCode")["Description"]
    .nunique()
)

missing_description = df_clean[df_clean["Description"].isna()]

recoverable_codes = missing_description["StockCode"].isin(
    description_by_code.index
)

print("\n3. Анализ пропущенных названий товаров:")
print("Всего строк без Description:", len(missing_description))
print(
    "Строк, для которых есть описание по StockCode:",
    recoverable_codes.sum()
)
print(
    "Строк, для которых нет описания по StockCode:",
    (~recoverable_codes).sum()
)

# 3. Проверяем, встречаются ли разные описания у одного StockCode
conflicting_codes = description_by_code[description_by_code > 1]

print("\n4. Проверка неоднозначных описаний:")
print("Кодов товаров с несколькими описаниями:", len(conflicting_codes))

# 4. Анализ пропусков CustomerID
missing_customer = df_clean["CustomerID"].isna()

print("\n5. Анализ CustomerID:")
print("Строк без CustomerID:", missing_customer.sum())
print(
    "Строк с CustomerID:",
    df_clean["CustomerID"].notna().sum()
)

print("\nЭТАП 8 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 9. Проверка возможности восстановления DESCRIPTION")
print("-" * 60)

# Подсчитываем частоту каждого описания для каждого кода товара
description_counts = (
    df_clean.dropna(subset=["Description"])
    .groupby(["StockCode", "Description"])
    .size()
    .reset_index(name="Count")
)

# Находим максимальную частоту описания для каждого товара
max_counts = description_counts.groupby("StockCode")["Count"].transform("max")

# Оставляем описания с максимальной частотой
top_descriptions = description_counts[
    description_counts["Count"] == max_counts
]

# Считаем, сколько вариантов имеют одинаковую максимальную частоту
top_counts = top_descriptions.groupby("StockCode").size()

# Коды, у которых только один наиболее частый вариант
unique_mode_codes = top_counts[top_counts == 1].index

# Коды, у которых несколько равнозначных вариантов
ambiguous_mode_codes = top_counts[top_counts > 1].index

# Проверяем пропуски Description
missing_description = df_clean[df_clean["Description"].isna()]

can_recover = missing_description["StockCode"].isin(unique_mode_codes)
cannot_recover = missing_description["StockCode"].isin(ambiguous_mode_codes)

print("Строк без Description:", len(missing_description))
print("Можно восстановить по однозначному наиболее частому описанию:",
      can_recover.sum())
print("Требуют дополнительной проверки:",
      cannot_recover.sum())

print("\nКоличество кодов с однозначным наиболее частым описанием:",
      len(unique_mode_codes))
print("Количество кодов с неоднозначным наиболее частым описанием:",
      len(ambiguous_mode_codes))

print("\nЭТАП 9 ЗАВЕРШЁН")

print("\n" + "-" * 60)
print("ЭТАП 10. Восстановление пропущенных DESCRIPTION")
print("-" * 60)

# 1. Создаём отдельную копию очищенной таблицы
df_final = df_clean.copy()

# 2. Определяем наиболее часто встречающееся описание
description_counts = (
    df_final.dropna(subset=["Description"])
    .groupby(["StockCode", "Description"])
    .size()
    .reset_index(name="Count")
)

# 3. Находим максимальную частоту для каждого StockCode
max_counts = (
    description_counts.groupby("StockCode")["Count"]
    .transform("max")
)

top_descriptions = description_counts[
    description_counts["Count"] == max_counts
]

# 4. Оставляем только коды с одним наиболее частым описанием
top_counts = top_descriptions.groupby("StockCode").size()

unique_mode_codes = top_counts[top_counts == 1].index

description_mapping = (
    top_descriptions[
        top_descriptions["StockCode"].isin(unique_mode_codes)
    ]
    .set_index("StockCode")["Description"]
)

# 5. Запоминаем количество пропусков до заполнения
missing_before = df_final["Description"].isna().sum()

# 6. Заполняем только пропуски с однозначным соответствием
df_final["Description"] = df_final["Description"].fillna(
    df_final["StockCode"].map(description_mapping)
)

# 7. Проверяем результат
missing_after = df_final["Description"].isna().sum()
restored = missing_before - missing_after

print("Пропусков Description до заполнения:", missing_before)
print("Восстановлено названий товаров:", restored)
print("Осталось пропусков Description:", missing_after)

# 8. Проверяем CustomerID — не заполняем его искусственно
print("\nПроверка CustomerID:")
print("Пропусков CustomerID:", df_final["CustomerID"].isna().sum())

# 9. Сохраняем результат в отдельный файл
df_final.to_csv(
    RESULTS_DIR / "Online_Retail_cleaned.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n Итоговая очищенная таблица сохранена.")
print("ЭТАП 10 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 11. Классификация аномальных операций")
print("-" * 60)

# Используем очищенную таблицу после этапа 10
df_classified = df_final.copy()

# 1. Определяем типы нестандартных операций
cancelled_mask = (
    df_classified["InvoiceNo"].astype(str).str.startswith("C")
)

negative_quantity_mask = df_classified["Quantity"] < 0
zero_price_mask = df_classified["UnitPrice"] == 0
negative_price_mask = df_classified["UnitPrice"] < 0

adjustment_mask = (
    df_classified["Description"]
    .str.contains(
        "Adjust bad debt",
        case=False,
        na=False
    )
)

# 2. Добавляем категорию каждой записи
df_classified["OperationType"] = "Обычная операция"

df_classified.loc[
    cancelled_mask, "OperationType"
] = "Отмена"

df_classified.loc[
    negative_quantity_mask & ~cancelled_mask,
    "OperationType"
] = "Отрицательное количество без отмены"

df_classified.loc[
    zero_price_mask, "OperationType"
] = "Нулевая цена"

df_classified.loc[
    negative_price_mask, "OperationType"
] = "Отрицательная цена"

df_classified.loc[
    adjustment_mask, "OperationType"
] = "Корректировка задолженности"

# 3. Выводим количество операций каждого типа
print("\n1. Распределение операций по категориям:")

print(
    df_classified["OperationType"]
    .value_counts()
    .to_string()
)

# 4. Проверяем основные виды аномалий отдельно
print("\n2. Проверка отдельных признаков:")

print("Отменённые операции:", cancelled_mask.sum())
print("Отрицательное количество:", negative_quantity_mask.sum())
print("Нулевая цена:", zero_price_mask.sum())
print("Отрицательная цена:", negative_price_mask.sum())
print("Корректировки задолженности:", adjustment_mask.sum())

# 5. Формируем отдельную таблицу обычных продаж
# Условия: операция не отменена, количество и цена положительные,
# запись не относится к корректировке задолженности.

regular_sales_mask = (
    ~cancelled_mask
    & (df_classified["Quantity"] > 0)
    & (df_classified["UnitPrice"] > 0)
    & ~adjustment_mask
)

df_sales = df_classified.loc[regular_sales_mask].copy()

# Рассчитываем выручку по каждой товарной строке
df_sales["Revenue"] = (
    df_sales["Quantity"] * df_sales["UnitPrice"]
)

# 6. Формируем отдельные таблицы нестандартных операций
df_cancelled = df_classified.loc[cancelled_mask].copy()

df_returns_or_adjustments = df_classified.loc[
    negative_quantity_mask & ~cancelled_mask
].copy()

df_zero_price = df_classified.loc[zero_price_mask].copy()

df_negative_price = df_classified.loc[negative_price_mask].copy()

df_adjustments = df_classified.loc[adjustment_mask].copy()

# 7. Выводим результаты формирования таблицы продаж
print("\n3. Формирование таблицы обычных продаж:")

print("Всего строк после очистки:", len(df_classified))
print("Строк, отнесённых к обычным продажам:", len(df_sales))
print("Строк отменённых операций:", len(df_cancelled))
print("Строк с отрицательным количеством без отмены:",
      len(df_returns_or_adjustments))
print("Строк с нулевой ценой:", len(df_zero_price))
print("Строк с отрицательной ценой:", len(df_negative_price))
print("Строк корректировок задолженности:", len(df_adjustments))

print("\n4. Первые строки таблицы обычных продаж:")
print(
    df_sales[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "Revenue"]
    ].head(10).to_string(index=False)
)

# 8. Сохраняем таблицы в папку results
df_classified.to_csv(
    RESULTS_DIR / "Online_Retail_classified.csv",
    index=False,
    encoding="utf-8-sig"
)

df_sales.to_csv(
    RESULTS_DIR / "Online_Retail_sales.csv",
    index=False,
    encoding="utf-8-sig"
)

df_cancelled.to_csv(
    RESULTS_DIR / "Cancelled_operations.csv",
    index=False,
    encoding="utf-8-sig"
)

df_returns_or_adjustments.to_csv(
    RESULTS_DIR / "Negative_quantity_operations.csv",
    index=False,
    encoding="utf-8-sig"
)

df_zero_price.to_csv(
    RESULTS_DIR / "Zero_price_operations.csv",
    index=False,
    encoding="utf-8-sig"
)

df_negative_price.to_csv(
    RESULTS_DIR / "Negative_price_operations.csv",
    index=False,
    encoding="utf-8-sig"
)

df_adjustments.to_csv(
    RESULTS_DIR / "Debt_adjustments.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nФайлы с результатами сохранены в папке results.")
print("ЭТАП 11 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 12. Итоговая проверка качества данных")
print("-" * 60)

# 1. Проверяем размер итоговой таблицы
print("\n1. Размер таблицы обычных продаж:")
print("Количество строк:", len(df_sales))
print("Количество столбцов:", len(df_sales.columns))

# 2. Проверяем типы данных
print("\n2. Типы данных:")
print(df_sales.dtypes)

# 3. Проверяем пропущенные значения
print("\n3. Пропущенные значения:")
print(df_sales.isnull().sum())

# 4. Проверяем отрицательные и нулевые значения
print("\n4. Проверка числовых показателей:")

print("Отрицательное количество:",
      (df_sales["Quantity"] < 0).sum())

print("Нулевое количество:",
      (df_sales["Quantity"] == 0).sum())

print("Отрицательная цена:",
      (df_sales["UnitPrice"] < 0).sum())

print("Нулевая цена:",
      (df_sales["UnitPrice"] == 0).sum())

print("Отрицательная выручка:",
      (df_sales["Revenue"] < 0).sum())

# 5. Проверяем корректность расчёта выручки
revenue_check = (
    df_sales["Revenue"]
    == df_sales["Quantity"] * df_sales["UnitPrice"]
)

print("\n5. Проверка расчёта выручки:")
print("Корректных расчётов:", revenue_check.sum())
print("Некорректных расчётов:", (~revenue_check).sum())

# 6. Основные характеристики набора данных
print("\n6. Основные показатели:")

print("Количество уникальных заказов:",
      df_sales["InvoiceNo"].nunique())

print("Количество уникальных товаров:",
      df_sales["StockCode"].nunique())

print("Количество уникальных покупателей:",
      df_sales["CustomerID"].nunique())

print("Количество стран:",
      df_sales["Country"].nunique())

# 7. Проверяем временной диапазон
print("\n7. Временной диапазон продаж:")
print("Первая дата:", df_sales["InvoiceDate"].min())
print("Последняя дата:", df_sales["InvoiceDate"].max())

# 8. Рассчитываем общую выручку
total_revenue = df_sales["Revenue"].sum()

print("\n8. Общая выручка:")
print(f"{total_revenue:,.2f}")

# 9. Формируем итоговую сводку
summary = pd.DataFrame({
    "Показатель": [
        "Количество строк",
        "Количество столбцов",
        "Количество заказов",
        "Количество товаров",
        "Количество покупателей",
        "Количество стран",
        "Общая выручка",
        "Пропуски CustomerID",
        "Пропуски Description"
    ],
    "Значение": [
        len(df_sales),
        len(df_sales.columns),
        df_sales["InvoiceNo"].nunique(),
        df_sales["StockCode"].nunique(),
        df_sales["CustomerID"].nunique(),
        df_sales["Country"].nunique(),
        total_revenue,
        df_sales["CustomerID"].isna().sum(),
        df_sales["Description"].isna().sum()
    ]
})

summary.to_csv(
    RESULTS_DIR / "Data_quality_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nИтоговая сводка сохранена в results.")
print("\nЭТАП 12 ЗАВЕРШЁН")
