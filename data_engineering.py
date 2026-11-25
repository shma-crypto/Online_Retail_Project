
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------
# ЭТАП 19. ИНЖЕНЕРИЯ ДАННЫХ
# ----------------------------------------------------------

print("\n" + "-" * 60)
print("ЭТАП 19. Формирование итогового аналитического набора")
print("-" * 60)

# 1. Определяем пути к файлам
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

SALES_PATH = RESULTS_DIR / "Online_Retail_sales.csv"
CUSTOMERS_PATH = RESULTS_DIR / "Customer_Analysis.csv"
RFM_PATH = RESULTS_DIR / "RFM_Analysis.csv"
PRODUCTS_PATH = RESULTS_DIR / "Product_Analysis.csv"

# Проверяем наличие необходимых файлов
required_files = [
    SALES_PATH,
    CUSTOMERS_PATH,
    RFM_PATH,
    PRODUCTS_PATH
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Не найден необходимый файл: {file_path}"
        )

# 2. Загружаем подготовленные данные
print("\n1. Загрузка данных")

sales = pd.read_csv(
    SALES_PATH,
    parse_dates=["InvoiceDate"]
)

customers = pd.read_csv(CUSTOMERS_PATH)
rfm = pd.read_csv(RFM_PATH)
products = pd.read_csv(PRODUCTS_PATH)

print("Продажи:", sales.shape)
print("Покупатели:", customers.shape)
print("RFM-анализ:", rfm.shape)
print("Товары:", products.shape)

# 3. Приводим ключи объединения к единому формату
sales["CustomerID"] = pd.to_numeric(
    sales["CustomerID"], errors="coerce"
).astype("Int64")

customers["CustomerID"] = pd.to_numeric(
    customers["CustomerID"], errors="coerce"
).astype("Int64")

rfm["CustomerID"] = pd.to_numeric(
    rfm["CustomerID"], errors="coerce"
).astype("Int64")

sales["StockCode"] = sales["StockCode"].astype(str)
products["StockCode"] = products["StockCode"].astype(str)

# 4. Проверяем уникальность ключей в справочниках
if customers["CustomerID"].duplicated().any():
    raise ValueError("В таблице покупателей найдены повторяющиеся CustomerID.")

if rfm["CustomerID"].duplicated().any():
    raise ValueError("В RFM-таблице найдены повторяющиеся CustomerID.")

if products["StockCode"].duplicated().any():
    raise ValueError("В таблице товаров найдены повторяющиеся StockCode.")

# 5. Выбираем показатели покупателей
customer_columns = customers[
    [
        "CustomerID",
        "TotalRevenue",
        "TotalQuantity",
        "Orders",
        "AverageOrderValue"
    ]
].rename(
    columns={
        "TotalRevenue": "CustomerTotalRevenue",
        "TotalQuantity": "CustomerTotalQuantity",
        "Orders": "CustomerOrders"
    }
)

# 6. Выбираем RFM-показатели
rfm_columns = rfm[
    [
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "R_Score",
        "F_Score",
        "M_Score",
        "RFM_Score",
        "Segment"
    ]
].rename(
    columns={
        "Frequency": "RFM_Frequency",
        "Monetary": "RFM_Monetary",
        "Segment": "RFMSegment"
    }
)

# 7. Выбираем характеристики товаров
product_columns = products[
    [
        "StockCode",
        "QuantitySold",
        "Revenue",
        "Orders",
        "AveragePrice"
    ]
].rename(
    columns={
        "QuantitySold": "ProductTotalQuantity",
        "Revenue": "ProductTotalRevenue",
        "Orders": "ProductOrders"
    }
)

# 8. Объединяем таблицы
print("\n2. Объединение данных")

analytical_data = sales.merge(
    customer_columns,
    on="CustomerID",
    how="left",
    validate="many_to_one"
)

analytical_data = analytical_data.merge(
    rfm_columns,
    on="CustomerID",
    how="left",
    validate="many_to_one"
)

analytical_data = analytical_data.merge(
    product_columns,
    on="StockCode",
    how="left",
    validate="many_to_one"
)

print("Размер итоговой таблицы:", analytical_data.shape)

# 9. Проверяем корректность объединения
print("\n3. Проверка качества итогового набора")

print("Строк до объединения:", len(sales))
print("Строк после объединения:", len(analytical_data))

if len(sales) != len(analytical_data):
    raise ValueError(
        "Количество строк изменилось после объединения данных."
    )

print(
    "Количество точных дубликатов:",
    analytical_data.duplicated().sum()
)

print(
    "Строк без CustomerID:",
    analytical_data["CustomerID"].isna().sum()
)

print(
    "Строк без RFM-сегмента:",
    analytical_data["RFMSegment"].isna().sum()
)

print(
    "Строк без характеристик товара:",
    analytical_data["ProductTotalRevenue"].isna().sum()
)

print(
    "Пропуски в итоговой таблице:",
    analytical_data.isna().sum().sum()
)

# Проверяем сохранение общей выручки
original_revenue = sales["Revenue"].sum()
final_revenue = analytical_data["Revenue"].sum()

print("\nИсходная выручка:", round(original_revenue, 2))
print("Выручка после объединения:", round(final_revenue, 2))

if not abs(original_revenue - final_revenue) < 0.01:
    raise ValueError("Выручка изменилась после объединения данных.")

# 10. Сохраняем итоговый аналитический набор
analytical_path = RESULTS_DIR / "Online_Retail_Analytical_Dataset.csv"

analytical_data.to_csv(
    analytical_path,
    index=False,
    encoding="utf-8-sig"
)

print("\nИтоговый аналитический набор сохранён:")
print(analytical_path)

# 11. Формируем сводную таблицу качества данных
quality_summary = pd.DataFrame({
    "Показатель": [
        "Количество строк исходных продаж",
        "Количество строк итогового набора",
        "Количество столбцов итогового набора",
        "Количество покупателей",
        "Количество товарных позиций",
        "Количество строк без CustomerID",
        "Количество строк без RFM-сегмента",
        "Количество строк без характеристик товара",
        "Количество точных дубликатов",
        "Общая выручка"
    ],
    "Значение": [
        len(sales),
        len(analytical_data),
        analytical_data.shape[1],
        analytical_data["CustomerID"].nunique(),
        analytical_data["StockCode"].nunique(),
        analytical_data["CustomerID"].isna().sum(),
        analytical_data["RFMSegment"].isna().sum(),
        analytical_data["ProductTotalRevenue"].isna().sum(),
        analytical_data.duplicated().sum(),
        round(final_revenue, 2)
    ]
})

# 12. Создаём итоговую книгу Excel со сводными таблицами
excel_path = RESULTS_DIR / "Online_Retail_Analytical_Summary.xlsx"

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    quality_summary.to_excel(
        writer,
        sheet_name="Data_Quality",
        index=False
    )

    customers.to_excel(
        writer,
        sheet_name="Customers",
        index=False
    )

    rfm.to_excel(
        writer,
        sheet_name="RFM",
        index=False
    )

    products.to_excel(
        writer,
        sheet_name="Products",
        index=False
    )

    pd.read_csv(RESULTS_DIR / "Monthly_Sales.csv").to_excel(
        writer,
        sheet_name="Monthly_Sales",
        index=False
    )

print("\nСводная книга Excel сохранена:")
print(excel_path)

print("\n" + "-" * 60)
print("ЭТАП 19. ИНЖЕНЕРИЯ ДАННЫХ ЗАВЕРШЕНА")
print("-" * 60)


print("\n4. Детальная проверка пропусков")

missing_by_column = (
    analytical_data.isna()
    .sum()
    .sort_values(ascending=False)
)

missing_report = pd.DataFrame({
    "MissingValues": missing_by_column,
    "MissingPercent": (
        missing_by_column / len(analytical_data) * 100
    ).round(2)
})

print(missing_report.to_string())

missing_report.to_csv(
    RESULTS_DIR / "Final_Missing_Values_Report.csv",
    encoding="utf-8-sig"
)

print("\nОтчёт о пропусках сохранён.")
