from __future__ import annotations

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from retail_lakehouse.analytics import (  # noqa: E402
    compute_category_performance,
    compute_kpis,
    compute_monthly_trend,
    compute_region_performance,
    compute_top_products,
    load_sales_data,
)
from retail_lakehouse.data_generator import generate_sales_data  # noqa: E402


DATA_PATH = ROOT / "data" / "retail_sales.csv"


@st.cache_data
def get_sales_frame() -> object:
    if not DATA_PATH.exists():
        generate_sales_data(output_path=DATA_PATH)
    return load_sales_data(DATA_PATH)


st.set_page_config(page_title="Retail Sales Analytics Lakehouse", layout="wide")

sales_df = get_sales_frame()
summary = compute_kpis(sales_df)
category_summary = compute_category_performance(sales_df)
monthly_trend = compute_monthly_trend(sales_df)
region_summary = compute_region_performance(sales_df)
products_summary = compute_top_products(sales_df, limit=5)

st.title("Retail Sales Analytics Lakehouse")
st.caption("Databricks + Snowflake architecture demo for retail performance monitoring")

st.markdown(
    """
    This dashboard simulates a modern lakehouse architecture that combines operational sales data,
    Databricks transformation workflows, and Snowflake-ready analytics views for business reporting.
    """
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${summary['total_revenue']:,.2f}")
col2.metric("Total Orders", f"{summary['total_orders']:,}")
col3.metric("Total Units", f"{summary['total_quantity']:,}")
col4.metric("Avg Order Value", f"${summary['avg_order_value']:,.2f}")

st.subheader("Revenue by category")
fig_category = px.bar(
    category_summary,
    x="category",
    y="revenue",
    color="category",
    title="Revenue contribution by product category",
)
st.plotly_chart(fig_category, use_container_width=True)

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Monthly revenue trend")
    fig_month = px.line(
        monthly_trend,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly revenue trend",
    )
    st.plotly_chart(fig_month, use_container_width=True)

with right_col:
    st.subheader("Regional sales")
    fig_region = px.bar(
        region_summary,
        x="region",
        y="revenue",
        color="region",
        title="Revenue by region",
    )
    st.plotly_chart(fig_region, use_container_width=True)

st.subheader("Top selling products")
fig_products = px.bar(
    products_summary,
    x="product",
    y="revenue",
    color="product",
    title="Top products by revenue",
)
st.plotly_chart(fig_products, use_container_width=True)

st.subheader("Current data snapshot")
st.dataframe(sales_df.head(10), use_container_width=True)
