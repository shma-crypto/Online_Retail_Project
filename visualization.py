
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Пути к папкам проекта
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
PLOTS_DIR = RESULTS_DIR / "plots"

# Создаём папку для графиков, если её ещё нет
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Общие настройки графиков
plt.rcParams["figure.figsize"] = (11, 6)
plt.rcParams["font.size"] = 10


def save_plot(filename):
    """Сохраняет текущий график и закрывает его."""
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Сохранён график: {filename}")


# --------------------------------------------------
# ГРАФИК 1. ДИНАМИКА ВЫРУЧКИ ПО МЕСЯЦАМ
# --------------------------------------------------

monthly = pd.read_csv(RESULTS_DIR / "Monthly_Sales.csv")

plt.figure()
plt.plot(
    monthly["YearMonth"],
    monthly["Revenue"],
    marker="o"
)
plt.title("Динамика выручки по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Выручка")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

save_plot("01_monthly_revenue.png")


# --------------------------------------------------
# ГРАФИК 2. ТОП-10 ТОВАРОВ ПО ВЫРУЧКЕ
# --------------------------------------------------

top_revenue = pd.read_csv(
    RESULTS_DIR / "Top_Products_Revenue.csv"
)

top_revenue = top_revenue.sort_values(
    "Revenue", ascending=True
)

plt.figure()
plt.barh(
    top_revenue["Description"].astype(str),
    top_revenue["Revenue"]
)
plt.title("Топ-10 товарных позиций по выручке")
plt.xlabel("Выручка")
plt.ylabel("Товарная позиция")

save_plot("02_top_products_revenue.png")


# --------------------------------------------------
# ГРАФИК 3. ТОП-10 ТОВАРОВ ПО КОЛИЧЕСТВУ ПРОДАЖ
# --------------------------------------------------
top_quantity = pd.read_csv(
    RESULTS_DIR / "Top_Products_Quantity.csv"
)

top_quantity = top_quantity.sort_values(
    "QuantitySold", ascending=True
)

plt.figure()
plt.barh(
    top_quantity["Description"].astype(str),
    top_quantity["QuantitySold"]
)
plt.title("Топ-10 товарных позиций по количеству продаж")
plt.xlabel("Количество проданных единиц")
plt.ylabel("Товарная позиция")

save_plot("03_top_products_quantity.png")


# --------------------------------------------------
# ГРАФИК 4. ТОП-10 ПОКУПАТЕЛЕЙ ПО ВЫРУЧКЕ
# --------------------------------------------------

top_customers = pd.read_csv(
    RESULTS_DIR / "Top_Customers_Revenue.csv"
)

top_customers = top_customers.sort_values(
    "TotalRevenue", ascending=True
)

plt.figure()
plt.barh(
    top_customers["CustomerID"].astype(str),
    top_customers["TotalRevenue"]
)
plt.title("Топ-10 покупателей по общей выручке")
plt.xlabel("Выручка")
plt.ylabel("Идентификатор покупателя")

save_plot("04_top_customers_revenue.png")


# --------------------------------------------------
# ГРАФИК 5. КОЛИЧЕСТВО ПОКУПАТЕЛЕЙ ПО RFM-СЕГМЕНТАМ
# --------------------------------------------------

rfm_segments = pd.read_csv(
    RESULTS_DIR / "RFM_Segments.csv"
)

rfm_segments = rfm_segments.sort_values(
    "Customers", ascending=True
)

plt.figure()
plt.barh(
    rfm_segments["Segment"],
    rfm_segments["Customers"]
)
plt.title("Распределение покупателей по RFM-сегментам")
plt.xlabel("Количество покупателей")
plt.ylabel("Сегмент")

save_plot("05_rfm_customers.png")


# --------------------------------------------------
# ГРАФИК 6. ВЫРУЧКА ПО RFM-СЕГМЕНТАМ
# --------------------------------------------------

rfm_revenue = rfm_segments.sort_values(
    "TotalRevenue", ascending=True
)

plt.figure()
plt.barh(
    rfm_revenue["Segment"],
    rfm_revenue["TotalRevenue"]
)
plt.title("Выручка по RFM-сегментам")
plt.xlabel("Общая выручка")
plt.ylabel("Сегмент")

save_plot("06_rfm_revenue.png")


print("\n" + "-" * 60)
print("ЭТАП 18. ВИЗУАЛИЗАЦИЯ ЗАВЕРШЕНА")
print("Все графики сохранены в:", PLOTS_DIR)
print("-" * 60)
