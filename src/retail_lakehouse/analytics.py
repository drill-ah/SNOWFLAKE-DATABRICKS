from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_sales_data(data_path: str | Path) -> pd.DataFrame:
    """Load sales data from csv and standardize the date and numeric types."""
    df = pd.read_csv(data_path, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    if "discount_rate" not in df.columns:
        df["discount_rate"] = 0.0
    return df


def compute_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Compute high-level metrics for the retail sales dashboard."""
    total_revenue = float(df["revenue"].sum())
    total_orders = int(df["order_id"].nunique())
    total_quantity = int(df["quantity"].sum())
    avg_order_value = round(total_revenue / total_orders, 2) if total_orders else 0.0
    avg_discount = round(float(df["discount_rate"].mean() * 100), 2)

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "avg_order_value": avg_order_value,
        "avg_discount_pct": avg_discount,
    }


def compute_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("category", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            quantity=("quantity", "sum"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend = (
        df.groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            quantity=("quantity", "sum"),
        )
        .sort_values("month")
        .reset_index(drop=True)
    )
    return trend


def compute_region_performance(df: pd.DataFrame) -> pd.DataFrame:
    performance = (
        df.groupby("region", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            quantity=("quantity", "sum"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    return performance


def compute_top_products(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    products = (
        df.groupby("product", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"), orders=("order_id", "nunique"))
        .sort_values("revenue", ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )
    return products
