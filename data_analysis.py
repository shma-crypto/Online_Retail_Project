import pandas as pd
from pathlib import Path

# Определяем путь к проекту
BASE_DIR = Path(__file__).resolve().parent

# Загружаем исходные данные
DATA_PATH = BASE_DIR / "Data" / "Online Retail.xlsx"

df = pd.read_excel(DATA_PATH)

print("-" * 60)
print("ЭТАП 2. Диагностика качества данных")
print("-" * 60)

# 1. Количество отрицательных значений Quantity
negative_quantity = (df["Quantity"] < 0).sum()

print("\nОтрицательное количество товаров:")
print(negative_quantity)

# 2. Количество нулевых значений Quantity
zero_quantity = (df["Quantity"] == 0).sum()

print("\nНулевое количество товаров:")
print(zero_quantity)

# 3. Отрицательные цены
negative_price = (df["UnitPrice"] < 0).sum()

print("\nОтрицательные цены:")
print(negative_price)

# 4. Нулевые цены
zero_price = (df["UnitPrice"] == 0).sum()

print("\nНулевые цены:")
print(zero_price)

# 5. Отменённые заказы
cancelled_orders = df["InvoiceNo"].astype(str).str.startswith("C").sum()

print("\nОтменённые операции:")
print(cancelled_orders)

# 6. Уникальные значения
print("\nКоличество уникальных заказов:")
print(df["InvoiceNo"].nunique())

print("\nКоличество уникальных товаров:")
print(df["StockCode"].nunique())

print("\nКоличество уникальных покупателей:")
print(df["CustomerID"].nunique())

print("\nКоличество стран:")
print(df["Country"].nunique())

# 7. Период данных
print("\nПериод исследования:")
print("Начало:", df["InvoiceDate"].min())
print("Окончание:", df["InvoiceDate"].max())

print("\nЭТАП 2 ЗАВЕРШЁН")


import pandas as pd
from pathlib import Path

print("\n" + "-" * 60)
print("ЭТАП 13. Общий анализ продаж")
print("-" * 60)

# 1. Определяем пути к файлам
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"

# 2. Загружаем подготовленную таблицу обычных продаж
DATA_PATH = RESULTS_DIR / "Online_Retail_sales.csv"

df_sales = pd.read_csv(
    DATA_PATH,
    encoding="utf-8-sig",
    parse_dates=["InvoiceDate"]
)

print("\n1. Информация о данных:")
print("Количество строк:", len(df_sales))
print("Количество столбцов:", len(df_sales.columns))

# 3. Рассчитываем основные показатели продаж
total_revenue = df_sales["Revenue"].sum()

total_quantity = df_sales["Quantity"].sum()

total_orders = df_sales["InvoiceNo"].nunique()

total_products = df_sales["StockCode"].nunique()

total_customers = df_sales["CustomerID"].nunique()

total_countries = df_sales["Country"].nunique()

# 4. Формируем таблицу заказов
orders = (
    df_sales.groupby("InvoiceNo")
    .agg(
        OrderRevenue=("Revenue", "sum"),
        OrderQuantity=("Quantity", "sum"),
        OrderDate=("InvoiceDate", "min"),
        CustomerID=("CustomerID", "first")
    )
    .reset_index()
)

# 5. Рассчитываем средние показатели
average_order_value = orders["OrderRevenue"].mean()

median_order_value = orders["OrderRevenue"].median()

average_quantity_per_order = orders["OrderQuantity"].mean()

average_line_revenue = df_sales["Revenue"].mean()

# 6. Выводим результаты
print("\n2. ОСНОВНЫЕ ПОКАЗАТЕЛИ ПРОДАЖ")

print(f"Общая выручка: {total_revenue:,.2f}")
print(f"Количество проданных единиц: {total_quantity:,}")
print(f"Количество заказов: {total_orders:,}")
print(f"Количество уникальных товаров: {total_products:,}")
print(f"Количество покупателей с известным ID: {total_customers:,}")
print(f"Количество стран: {total_countries}")

print("\n3. ПОКАЗАТЕЛИ СРЕДНЕГО ЗАКАЗА")

print(f"Средняя сумма заказа: {average_order_value:,.2f}")
print(f"Медианная сумма заказа: {median_order_value:,.2f}")
print(f"Среднее количество единиц в заказе: {average_quantity_per_order:.2f}")
print(f"Средняя выручка на товарную строку: {average_line_revenue:,.2f}")

# 7. Формируем итоговую таблицу показателей
kpi = pd.DataFrame({
    "Показатель": [
        "Общая выручка",
        "Количество проданных единиц",
        "Количество заказов",
        "Количество уникальных товаров",
        "Количество покупателей с известным ID",
        "Количество стран",
        "Средняя сумма заказа",
        "Медианная сумма заказа",
        "Среднее количество единиц в заказе",
        "Средняя выручка на товарную строку"
    ],
    "Значение": [
        total_revenue,
        total_quantity,
        total_orders,
        total_products,
        total_customers,
        total_countries,
        average_order_value,
        median_order_value,
        average_quantity_per_order,
        average_line_revenue
    ]
})

# 8. Сохраняем результаты
kpi.to_csv(
    RESULTS_DIR / "Sales_KPI.csv",
    index=False,
    encoding="utf-8-sig"
)

orders.to_csv(
    RESULTS_DIR / "Orders_Analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nФайлы Sales_KPI.csv и Orders_Analysis.csv сохранены.")
print("\nЭТАП 13 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 14. Анализ динамики продаж")
print("-" * 60)

# 1. Подготовка даты
df_sales["InvoiceDate"] = pd.to_datetime(df_sales["InvoiceDate"])

# Создаём дополнительные временные признаки
df_sales["YearMonth"] = (
    df_sales["InvoiceDate"].dt.to_period("M").astype(str)
)

df_sales["Weekday"] = df_sales["InvoiceDate"].dt.day_of_week

df_sales["WeekdayName"] = (
    df_sales["InvoiceDate"].dt.day_name()
)

df_sales["Hour"] = df_sales["InvoiceDate"].dt.hour


# 2. Анализ продаж по месяцам
monthly_sales = (
    df_sales.groupby("YearMonth")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

print("\n1. Динамика продаж по месяцам")
print(monthly_sales.to_string(index=False))

# Находим лучший и худший месяцы по выручке
best_month = monthly_sales.loc[
    monthly_sales["Revenue"].idxmax()
]

worst_month = monthly_sales.loc[
    monthly_sales["Revenue"].idxmin()
]

print("\nМесяц с максимальной выручкой:")
print(best_month.to_string())

print("\nМесяц с минимальной выручкой:")
print(worst_month.to_string())


# 3. Анализ продаж по дням недели
weekday_sales = (
    df_sales.groupby(["Weekday", "WeekdayName"])
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Weekday")
)

print("\n2. Продажи по дням недели")
print(weekday_sales.to_string(index=False))

best_weekday = weekday_sales.loc[
    weekday_sales["Revenue"].idxmax()
]

print("\nДень недели с максимальной выручкой:")
print(best_weekday.to_string())


# 4. Анализ продаж по часам
hourly_sales = (
    df_sales.groupby("Hour")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

print("\n3. Продажи по часам")
print(hourly_sales.to_string(index=False))

best_hour = hourly_sales.loc[
    hourly_sales["Revenue"].idxmax()
]

print("\nЧас с максимальной выручкой:")
print(best_hour.to_string())


# 5. Сохраняем результаты
monthly_sales.to_csv(
    RESULTS_DIR / "Monthly_Sales.csv",
    index=False,
    encoding="utf-8-sig"
)

weekday_sales.to_csv(
    RESULTS_DIR / "Weekday_Sales.csv",
    index=False,
    encoding="utf-8-sig"
)

hourly_sales.to_csv(
    RESULTS_DIR / "Hourly_Sales.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nТаблицы временного анализа сохранены в results.")
print("\nЭТАП 14 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 15. Анализ товарного ассортимента")
print("-" * 60)

# 1. Загружаем подготовленную таблицу, если df_sales уже не загружена
# В рамках одного запуска этапы 13 и 14 уже создали df_sales.

# 2. Формируем сводную таблицу по товарам
product_analysis = (
    df_sales.groupby("StockCode")
    .agg(
        Description=("Description", "first"),
        QuantitySold=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique"),
        AveragePrice=("UnitPrice", "mean")
    )
    .reset_index()
)

print("\n1. Общая информация о товарах")
print("Количество уникальных товарных кодов:",
      product_analysis["StockCode"].nunique())

# 3. Топ-10 товаров по количеству проданных единиц
top_quantity = (
    product_analysis
    .sort_values("QuantitySold", ascending=False)
    .head(10)
)

print("\n2. ТОП-10 товаров по количеству продаж")
print(
    top_quantity[
        ["StockCode", "Description", "QuantitySold", "Revenue"]
    ].to_string(index=False)
)

# 4. Топ-10 товаров по выручке
top_revenue = (
    product_analysis
    .sort_values("Revenue", ascending=False)
    .head(10)
)

print("\n3. ТОП-10 товаров по выручке")
print(
    top_revenue[
        ["StockCode", "Description", "Revenue", "QuantitySold"]
    ].to_string(index=False)
)

# 5. Топ-10 товаров по количеству заказов
top_orders = (
    product_analysis
    .sort_values("Orders", ascending=False)
    .head(10)
)

print("\n4. ТОП-10 товаров по количеству заказов")
print(
    top_orders[
        ["StockCode", "Description", "Orders", "Revenue"]
    ].to_string(index=False)
)

# 6. Товары с наименьшим количеством проданных единиц
bottom_quantity = (
    product_analysis
    .sort_values(["QuantitySold", "Revenue"], ascending=True)
    .head(10)
)

print("\n5. 10 Товаров с наименьшим количеством продаж")
print(
    bottom_quantity[
        ["StockCode", "Description", "QuantitySold", "Revenue"]
    ].to_string(index=False)
)

# 7. Рассчитываем долю топ-10 товаров в общей выручке
total_revenue = df_sales["Revenue"].sum()

top10_revenue_sum = top_revenue["Revenue"].sum()

top10_revenue_share = (
    top10_revenue_sum / total_revenue * 100
)

print("\n6. Доля ТОП-10 товаров в общей выручке")
print(f"Выручка топ-10 товаров: {top10_revenue_sum:,.2f}")
print(f"Общая выручка: {total_revenue:,.2f}")
print(f"Доля топ-10 товаров: {top10_revenue_share:.2f}%")

# 8. Сохраняем результаты
product_analysis.to_csv(
    RESULTS_DIR / "Product_Analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

top_quantity.to_csv(
    RESULTS_DIR / "Top_Products_Quantity.csv",
    index=False,
    encoding="utf-8-sig"
)

top_revenue.to_csv(
    RESULTS_DIR / "Top_Products_Revenue.csv",
    index=False,
    encoding="utf-8-sig"
)

top_orders.to_csv(
    RESULTS_DIR / "Top_Products_Orders.csv",
    index=False,
    encoding="utf-8-sig"
)

bottom_quantity.to_csv(
    RESULTS_DIR / "Bottom_Products.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nРезультаты анализа ассортимента сохранены в results.")
print("\nЭТАП 15 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 16. Анализ покупательского поведения")
print("-" * 60)

# 1. Оставляем только записи с известным CustomerID
df_customers = df_sales.dropna(subset=["CustomerID"]).copy()

# Приводим CustomerID к целочисленному формату
df_customers["CustomerID"] = (
    df_customers["CustomerID"].astype("int64")
)

print("\n1. Общая информация")
print("Строк с известным CustomerID:", len(df_customers))
print("Количество покупателей:", df_customers["CustomerID"].nunique())

# 2. Формируем таблицу заказов покупателей
customer_orders = (
    df_customers.groupby(["CustomerID", "InvoiceNo"])
    .agg(
        OrderRevenue=("Revenue", "sum"),
        OrderQuantity=("Quantity", "sum"),
        OrderDate=("InvoiceDate", "min")
    )
    .reset_index()
)

# 3. Формируем сводную таблицу покупателей
customer_analysis = (
    df_customers.groupby("CustomerID")
    .agg(
        TotalRevenue=("Revenue", "sum"),
        TotalQuantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
        FirstPurchase=("InvoiceDate", "min"),
        LastPurchase=("InvoiceDate", "max"),
        Country=("Country", "first")
    )
    .reset_index()
)

# 4. Рассчитываем среднюю сумму заказа каждого покупателя
customer_analysis["AverageOrderValue"] = (
    customer_analysis["TotalRevenue"]
    / customer_analysis["Orders"]
)

# 5. Топ-10 покупателей по общей выручке
top_customers_revenue = (
    customer_analysis
    .sort_values("TotalRevenue", ascending=False)
    .head(10)
)

print("\n2. ТОП-10 покупателей по выручке")
print(
    top_customers_revenue[
        ["CustomerID", "TotalRevenue", "Orders",
         "TotalQuantity", "AverageOrderValue", "Country"]
    ].to_string(index=False)
)

# 6. Топ-10 покупателей по количеству заказов
top_customers_orders = (
    customer_analysis
    .sort_values("Orders", ascending=False)
    .head(10)
)

print("\n3. ТОП-10 покупателей по количестьву заказов")
print(
    top_customers_orders[
        ["CustomerID", "Orders", "TotalRevenue",
         "TotalQuantity", "Country"]
    ].to_string(index=False)
)

# 7. Топ-10 покупателей по количеству приобретённых единиц
top_customers_quantity = (
    customer_analysis
    .sort_values("TotalQuantity", ascending=False)
    .head(10)
)

print("\n4. ТОП-10 покупателей по количеству товаров")
print(
    top_customers_quantity[
        ["CustomerID", "TotalQuantity", "TotalRevenue",
         "Orders", "Country"]
    ].to_string(index=False)
)

# 8. Общие показатели покупательской активности
print("\n5. Общие показатели покупателей")

print(
    "Средняя выручка на покупателя:",
    round(customer_analysis["TotalRevenue"].mean(), 2)
)

print(
    "Медианная выручка на покупателя:",
    round(customer_analysis["TotalRevenue"].median(), 2)
)

print(
    "Среднее количество заказов на покупателя:",
    round(customer_analysis["Orders"].mean(), 2)
)

print(
    "Средний объём покупок на покупателя:",
    round(customer_analysis["TotalQuantity"].mean(), 2)
)

print(
    "Средний чек по заказам известных покупателей:",
    round(customer_orders["OrderRevenue"].mean(), 2)
)

# 9. Сегментация покупателей по сумме покупок
# Делим покупателей на 3 группы по терцилям выручки
customer_analysis["Segment"] = pd.qcut(
    customer_analysis["TotalRevenue"].rank(method="first"),
    q=3,
    labels=["Низкая выручка", "Средняя выручка", "Высокая выручка"]
)

segments = (
    customer_analysis.groupby("Segment", observed=False)
    .agg(
        Customers=("CustomerID", "count"),
        TotalRevenue=("TotalRevenue", "sum"),
        AverageRevenue=("TotalRevenue", "mean"),
        AverageOrders=("Orders", "mean")
    )
    .reset_index()
)

print("\n6. Сегментация покупателей")
print(segments.to_string(index=False))

# 10. Сохраняем результаты
customer_analysis.to_csv(
    RESULTS_DIR / "Customer_Analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

customer_orders.to_csv(
    RESULTS_DIR / "Customer_Orders.csv",
    index=False,
    encoding="utf-8-sig"
)

top_customers_revenue.to_csv(
    RESULTS_DIR / "Top_Customers_Revenue.csv",
    index=False,
    encoding="utf-8-sig"
)

top_customers_orders.to_csv(
    RESULTS_DIR / "Top_Customers_Orders.csv",
    index=False,
    encoding="utf-8-sig"
)

top_customers_quantity.to_csv(
    RESULTS_DIR / "Top_Customers_Quantity.csv",
    index=False,
    encoding="utf-8-sig"
)

segments.to_csv(
    RESULTS_DIR / "Customer_Segments.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nРезультаты анализа покупателей сохранены в results.")
print("\nЭТАП 16 ЗАВЕРШЁН")


print("\n" + "-" * 60)
print("ЭТАП 17. RFM-анализ покупателей")
print("-" * 60)

# 1. Используем только покупки с известным CustomerID
df_rfm = df_sales.dropna(subset=["CustomerID"]).copy()
df_rfm["CustomerID"] = df_rfm["CustomerID"].astype("int64")

# 2. Определяем условную дату анализа:
# следующий день после последней даты в наборе данных
reference_date = df_rfm["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

print("\nДата, относительно которой рассчитывается Recency:",
      reference_date.date())

# 3. Рассчитываем R, F и M для каждого покупателя
rfm = (
    df_rfm.groupby("CustomerID")
    .agg(
        Recency=("InvoiceDate", lambda x: (
            reference_date - x.max().normalize()
        ).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum")
    )
    .reset_index()
)

print("\n1. Общая информация")
print("Количество покупателей:", len(rfm))
print("Минимальная давность покупки:", rfm["Recency"].min(), "дней")
print("Максимальная давность покупки:", rfm["Recency"].max(), "дней")

# 4. Присваиваем оценки от 1 до 5
# Для Recency меньшее значение лучше,
# для Frequency и Monetary большее значение лучше.

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# 5. Рассчитываем общий RFM-балл
rfm["RFM_Score"] = (
    rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
)

# 6. Формируем группы покупателей
def define_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Лучшие покупатели"
    elif r >= 3 and f >= 4:
        return "Лояльные покупатели"
    elif r >= 4 and f <= 3:
        return "Перспективные покупатели"
    elif r <= 2 and f >= 3:
        return "Покупатели под риском"
    elif r <= 2 and f <= 2:
        return "Неактивные покупатели"
    else:
        return "Обычные покупатели"

rfm["Segment"] = rfm.apply(define_segment, axis=1)

# 7. Выводим 10 лучших покупателей по RFM-баллу
top_rfm = (
    rfm.sort_values(
        ["RFM_Score", "Monetary"],
        ascending=[False, False]
    )
    .head(10)
)

print("\n2. ТОП-10 покупателей по RFM-БАЛЛУ")
print(
    top_rfm[
        ["CustomerID", "Recency", "Frequency", "Monetary",
         "R_Score", "F_Score", "M_Score", "RFM_Score", "Segment"]
    ].to_string(index=False)
)

# 8. Сводная таблица по сегментам
rfm_segments = (
    rfm.groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        AverageRecency=("Recency", "mean"),
        AverageFrequency=("Frequency", "mean"),
        TotalRevenue=("Monetary", "sum"),
        AverageMonetary=("Monetary", "mean")
    )
    .reset_index()
    .sort_values("TotalRevenue", ascending=False)
)

print("\n3. Распределение по сегментам")
print(rfm_segments.to_string(index=False))

# 9. Сохраняем результаты
rfm.to_csv(
    RESULTS_DIR / "RFM_Analysis.csv",
    index=False,
    encoding="utf-8-sig"
)

top_rfm.to_csv(
    RESULTS_DIR / "Top_RFM_Customers.csv",
    index=False,
    encoding="utf-8-sig"
)

rfm_segments.to_csv(
    RESULTS_DIR / "RFM_Segments.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nРезультаты RFM-анализа сохранены в results.")
print("\nЭТАП 17 ЗАВЕРШЁН")
