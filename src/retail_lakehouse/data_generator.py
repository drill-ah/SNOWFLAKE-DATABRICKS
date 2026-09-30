from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_sales_data(n_rows: int = 2000, output_path: str | Path = "data/retail_sales.csv") -> pd.DataFrame:
    """Generate a synthetic retail sales dataset for analytics and dashboarding."""
    rng = np.random.default_rng(42)

    stores = [
        "New York",
        "Chicago",
        "Austin",
        "Seattle",
        "Miami",
        "Denver",
    ]
    region_map = {
        "New York": "Northeast",
        "Chicago": "Midwest",
        "Austin": "South",
        "Seattle": "West",
        "Miami": "South",
        "Denver": "West",
    }

    product_catalog = [
        ("Laptop", "Electronics", 899.00),
        ("Smartphone", "Electronics", 699.00),
        ("Tablet", "Electronics", 399.00),
        ("Headphones", "Electronics", 149.00),
        ("Desk Chair", "Furniture", 249.00),
        ("Office Desk", "Furniture", 829.00),
        ("Bookshelf", "Furniture", 529.00),
        ("Coffee Maker", "Home Goods", 129.00),
        ("Vacuum Cleaner", "Home Goods", 259.00),
        ("Air Purifier", "Home Goods", 189.00),
        ("Running Shoes", "Apparel", 129.00),
        ("Jacket", "Apparel", 179.00),
    ]
    weights = np.array([0.10, 0.12, 0.08, 0.10, 0.08, 0.07, 0.06, 0.10, 0.08, 0.07, 0.08, 0.06])

    order_dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    rows = []

    for idx in range(1, n_rows + 1):
        order_date = pd.Timestamp(rng.choice(order_dates))
        store_name = rng.choice(stores)
        region = region_map[store_name]
        selected_index = int(rng.choice(len(product_catalog), p=weights))
        product_name, category, base_price = product_catalog[selected_index]
        quantity = int(rng.integers(1, 9))
        unit_price = round(float(base_price * rng.uniform(0.88, 1.20)), 2)
        discount_rate = round(float(rng.uniform(0.04, 0.24)), 4)
        revenue = round(unit_price * quantity * (1 - discount_rate), 2)

        rows.append(
            {
                "order_id": f"ORD-{idx:06d}",
                "order_date": order_date.strftime("%Y-%m-%d"),
                "store": store_name,
                "region": region,
                "category": category,
                "product": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_rate": discount_rate,
                "revenue": revenue,
                "orders": 1,
            }
        )

    df = pd.DataFrame(rows)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    return df
