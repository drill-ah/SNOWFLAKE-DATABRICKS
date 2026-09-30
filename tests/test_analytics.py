from pathlib import Path

from retail_lakehouse.analytics import (
    compute_category_performance,
    compute_kpis,
    compute_monthly_trend,
    load_sales_data,
)
from retail_lakehouse.data_generator import generate_sales_data


def test_kpis_and_trend_generation(tmp_path):
    data_path = tmp_path / "retail_sales.csv"
    generate_sales_data(250, str(data_path))

    df = load_sales_data(data_path)
    assert not df.empty
    assert {"revenue", "orders", "quantity"}.issubset(df.columns)

    kpis = compute_kpis(df)
    assert kpis["total_revenue"] > 0
    assert kpis["total_orders"] > 0
    assert kpis["total_quantity"] > 0

    category_summary = compute_category_performance(df)
    assert not category_summary.empty
    assert "category" in category_summary.columns
    assert "revenue" in category_summary.columns

    trend = compute_monthly_trend(df)
    assert not trend.empty
    assert "month" in trend.columns
    assert "revenue" in trend.columns
