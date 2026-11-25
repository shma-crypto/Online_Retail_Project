
from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# ЭТАП 22. ПОЛНЫЙ ОТЧЁТ О ДАННЫХ И ПРЕОБРАЗОВАНИЯХ
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(exist_ok=True)

print("\n" + "-" * 65)
print("ЭТАП 22. ПОЛНЫЙ ОТЧЁТ О ДАННЫХ И ПРЕОБРАЗОВАНИЯХ")
print("-" * 65)

# ----------------------------------------------------------
# 1. ЗАГРУЗКА ИСХОДНЫХ И ИТОГОВЫХ ДАННЫХ
# ----------------------------------------------------------

raw_path = DATA_DIR / "Online Retail.xlsx"
sales_path = RESULTS_DIR / "Online_Retail_sales.csv"
final_path = RESULTS_DIR / "Online_Retail_Analytical_Dataset.csv"

required_files = [raw_path, sales_path, final_path]

for path in required_files:
    if not path.exists():
        raise FileNotFoundError(f"Не найден файл: {path}")

raw = pd.read_excel(raw_path)
sales = pd.read_csv(sales_path, parse_dates=["InvoiceDate"])
final = pd.read_csv(final_path)

print("\n1. Исходные и итоговые данные")
print("Исходный набор:", raw.shape)
print("Таблица продаж:", sales.shape)
print("Итоговый набор:", final.shape)

# ----------------------------------------------------------
# 2. ПРОФИЛЬ ИСХОДНЫХ ДАННЫХ
# ----------------------------------------------------------

source_profile = pd.DataFrame({
    "Показатель": [
        "Источник данных",
        "Количество строк",
        "Количество столбцов",
        "Количество пропусков",
        "Количество полных дубликатов",
        "Количество уникальных заказов",
        "Количество товарных кодов",
        "Количество покупателей",
        "Количество стран",
        "Начальная дата",
        "Конечная дата"
    ],
    "Значение": [
        "UCI Online Retail",
        len(raw),
        raw.shape[1],
        int(raw.isna().sum().sum()),
        int(raw.duplicated().sum()),
        raw["InvoiceNo"].nunique(),
        raw["StockCode"].nunique(),
        raw["CustomerID"].nunique(),
        raw["Country"].nunique(),
        str(pd.to_datetime(raw["InvoiceDate"]).min()),
        str(pd.to_datetime(raw["InvoiceDate"]).max())
    ]
})

print("\n2. Профиль исходных данных")
print(source_profile.to_string(index=False))

# ----------------------------------------------------------
# 3. ЖУРНАЛ ПРЕОБРАЗОВАНИЙ
# ----------------------------------------------------------

transformation_log = pd.DataFrame([
    {
        "Этап": 1,
        "Операция": "Загрузка исходных данных",
        "Описание": "Чтение файла Online Retail.xlsx средствами Pandas",
        "Результат": f"{len(raw)} строк, {raw.shape[1]} столбцов"
    },
    {
        "Этап": 2,
        "Операция": "Диагностика качества",
        "Описание": "Анализ пропусков, дубликатов, отрицательных и нулевых значений",
        "Результат": "Выявлены проблемы качества исходных данных"
    },
    {
        "Этап": 3,
        "Операция": "Удаление точных дубликатов",
        "Описание": "Удаление полностью совпадающих строк",
        "Результат": "Удалено 5 268 повторных строк"
    },
    {
        "Этап": 4,
        "Операция": "Обработка пропусков",
        "Описание": "Анализ отсутствующих описаний и идентификаторов покупателей",
        "Результат": "Восстановлено 1 339 описаний товаров; неустранимые пропуски сохранены"
    },
    {
        "Этап": 5,
        "Операция": "Классификация операций",
        "Описание": "Разделение обычных продаж, отмен, нулевых цен и корректировок",
        "Результат": "Сформированы отдельные категории операций"
    },
    {
        "Этап": 6,
        "Операция": "Формирование таблицы продаж",
        "Описание": "Исключение отменённых и некорректных для анализа продаж операций",
        "Результат": f"{len(sales)} строк обычных продаж"
    },
    {
        "Этап": 7,
        "Операция": "Создание признака Revenue",
        "Описание": "Расчёт выручки как произведения Quantity и UnitPrice",
        "Результат": f"Общая выручка {sales['Revenue'].sum():.2f}"
    },
    {
        "Этап": 8,
        "Операция": "Временные признаки",
        "Описание": "Создание YearMonth, Weekday, WeekdayName и Hour",
        "Результат": "Подготовлены признаки для анализа динамики продаж"
    },
    {
        "Этап": 9,
        "Операция": "Агрегирование товаров",
        "Описание": "Группировка по StockCode",
        "Результат": f"{sales['StockCode'].nunique()} товарных кодов"
    },
    {
        "Этап": 10,
        "Операция": "Агрегирование покупателей",
        "Описание": "Расчёт выручки, количества заказов и объёма покупок по CustomerID",
        "Результат": f"{sales['CustomerID'].nunique()} идентифицированных покупателей"
    },
    {
        "Этап": 11,
        "Операция": "RFM-анализ",
        "Описание": "Расчёт Recency, Frequency, Monetary и сегментов покупателей",
        "Результат": "Сформированы шесть клиентских сегментов"
    },
    {
        "Этап": 12,
        "Операция": "Инженерия данных",
        "Описание": "Объединение таблиц продаж, покупателей, товаров и RFM",
        "Результат": f"{final.shape[0]} строк, {final.shape[1]} столбцов"
    },
    {
        "Этап": 13,
        "Операция": "Статистика NumPy",
        "Описание": "Расчёт среднего, медианы, дисперсии, стандартного отклонения и квартилей",
        "Результат": "Рассчитаны характеристики трёх числовых признаков"
    },
    {
        "Этап": 14,
        "Операция": "Стандартизация и нормализация",
        "Описание": "Z-score, Robust Z-score, Modified Z-score, Mean, Unit Variance, L1, L2, Max и Probability",
        "Результат": "Сформированы преобразованные массивы"
    },
    {
        "Этап": 15,
        "Операция": "Контроль качества",
        "Описание": "Проверка размеров, выручки, пропусков и дубликатов",
        "Результат": "Количество строк и общая выручка сохранены"
    }
])

print("\n3. Журнал преобразований")
print(transformation_log.to_string(index=False))

# ----------------------------------------------------------
# 4. ПРОВЕРКА ИТОГОВОГО АНАЛИТИЧЕСКОГО НАБОРА
# ----------------------------------------------------------

original_revenue = sales["Revenue"].sum()
final_revenue = final["Revenue"].sum()

quality_checks = pd.DataFrame([
    {
        "Проверка": "Количество строк до объединения",
        "Результат": len(sales),
        "Статус": "Пройдена"
    },
    {
        "Проверка": "Количество строк после объединения",
        "Результат": len(final),
        "Статус": "Пройдена" if len(sales) == len(final) else "Ошибка"
    },
    {
        "Проверка": "Полные дубликаты итоговой таблицы",
        "Результат": int(final.duplicated().sum()),
        "Статус": "Пройдена" if final.duplicated().sum() == 0 else "Проверить"
    },
    {
        "Проверка": "Выручка исходной таблицы продаж",
        "Результат": round(original_revenue, 2),
        "Статус": "Контрольное значение"
    },
    {
        "Проверка": "Выручка после объединения",
        "Результат": round(final_revenue, 2),
        "Статус": "Пройдена" if np.isclose(original_revenue, final_revenue) else "Ошибка"
    },
    {
        "Проверка": "Строк без CustomerID",
        "Результат": int(final["CustomerID"].isna().sum()),
        "Статус": "Объясняется отсутствием ID в исходных данных"
    },
    {
        "Проверка": "Строк без характеристик товара",
        "Результат": int(final["ProductTotalRevenue"].isna().sum()),
        "Статус": "Пройдена" if final["ProductTotalRevenue"].isna().sum() == 0 else "Проверить"
    }
])

print("\n4. ПРОВЕРКА КАЧЕСТВА")
print(quality_checks.to_string(index=False))

# ----------------------------------------------------------
# 5. РЕЗУЛЬТАТЫ NUMPY
# ----------------------------------------------------------

numpy_files = {
    "Статистика": "NumPy_Statistics.csv",
    "Качество данных": "NumPy_Data_Quality.csv",
    "Преобразованные данные": "NumPy_Transformed_Data.csv",
    "Информационный отчёт": "NumPy_Information_Report.csv"
}

numpy_results = {}

for name, filename in numpy_files.items():
    path = RESULTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Не найден результат NumPy: {filename}"
        )
    numpy_results[name] = pd.read_csv(path)

numpy_methods = pd.DataFrame([
    ["Z-score", "Стандартизация по среднему и стандартному отклонению"],
    ["Robust Z-score", "Масштабирование относительно медианы и MAD"],
    ["Modified Z-score", "Выявление потенциальных выбросов"],
    ["Mean Normalization", "Преобразование относительно среднего и диапазона"],
    ["Unit Variance Scaling", "Масштабирование до единичной дисперсии"],
    ["L1 Normalization", "Нормализация строк по L1-норме"],
    ["L2 Normalization", "Нормализация строк по L2-норме"],
    ["Max Normalization", "Деление признака на максимальное значение"],
    ["Probability Normalization", "Нормализация столбцов до суммы 1"],
    ["Статистический анализ", "Среднее, медиана, дисперсия, квартили и диапазон"]
], columns=["Метод", "Описание"])

# ----------------------------------------------------------
# 6. СПИСОК СОЗДАННЫХ РЕЗУЛЬТАТОВ
# ----------------------------------------------------------

output_files = []

for path in sorted(RESULTS_DIR.rglob("*")):
    if path.is_file():
        output_files.append({
            "Файл": str(path.relative_to(RESULTS_DIR)),
            "Расширение": path.suffix,
            "Размер, КБ": round(path.stat().st_size / 1024, 2)
        })

outputs_df = pd.DataFrame(output_files)

# ----------------------------------------------------------
# 7. СОХРАНЕНИЕ ПОЛНОГО ОТЧЁТА В EXCEL
# ----------------------------------------------------------

excel_path = RESULTS_DIR / "Full_Data_Transformation_Report.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    source_profile.to_excel(
        writer, sheet_name="Source_Profile", index=False
    )

    transformation_log.to_excel(
        writer, sheet_name="Transformations", index=False
    )

    quality_checks.to_excel(
        writer, sheet_name="Quality_Checks", index=False
    )

    numpy_methods.to_excel(
        writer, sheet_name="NumPy_Methods", index=False
    )

    for name, table in numpy_results.items():
        sheet_name = name[:31]

        if name == "Преобразованные данные":
            table.head(1000).to_excel(
                writer, sheet_name=sheet_name, index=False
            )
        else:
            table.to_excel(
                writer, sheet_name=sheet_name, index=False
            )
    outputs_df.to_excel(
        writer, sheet_name="Output_Files", index=False
    )

# ----------------------------------------------------------
# 8. СОЗДАНИЕ ТЕКСТОВОГО ОТЧЁТА
# ----------------------------------------------------------

text_path = RESULTS_DIR / "Full_Data_Transformation_Report.txt"

with open(text_path, "w", encoding="utf-8") as file:
    file.write("ПОЛНЫЙ ОТЧЁТ О ДАННЫХ И ПРЕОБРАЗОВАНИЯХ\n")
    file.write("-" * 65 + "\n\n")

    file.write("1. Исходные данные\n")
    file.write(source_profile.to_string(index=False))
    file.write("\n\n")

    file.write("2. Выполненные преобразования\n")
    file.write(transformation_log.to_string(index=False))
    file.write("\n\n")

    file.write("3. Проверка качества итогового набора\n")
    file.write(quality_checks.to_string(index=False))
    file.write("\n\n")

    file.write("4. Методы NUMPY\n")
    file.write(numpy_methods.to_string(index=False))
    file.write("\n\n")

    file.write("5. Итоговые характеристики\n")
    file.write(f"Количество строк: {len(final)}\n")
    file.write(f"Количество столбцов: {final.shape[1]}\n")
    file.write(f"Общая выручка: {final_revenue:.2f}\n")
    file.write(f"Полные дубликаты: {final.duplicated().sum()}\n")

print("\n" + "-" * 65)
print("ЭТАП 22. Отчет сформирован")
print("-" * 65)

print("\nСозданы файлы:")
print(excel_path)
print(text_path)

print("\nКоличество строк итогового набора:", len(final))
print("Количество столбцов:", final.shape[1])
print("Общая выручка:", round(final_revenue, 2))

print("\nЭТАП 22 ЗАВЕРШЁН")
