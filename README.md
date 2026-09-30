# Retail Sales Analytics Lakehouse using Databricks and Snowflake

This project is a submission-ready retail analytics solution built around a modern lakehouse architecture using Databricks, Snowflake, and a Streamlit dashboard.

## Project objective
The goal is to design an end-to-end retail analytics workflow that enables:

- ingestion of sales data
- transformation in a lakehouse environment
- analytical reporting in Snowflake
- business-facing dashboarding for KPI tracking

## Business context
The solution models a retail business that needs to monitor:

- revenue by category and region
- order volume and unit sales trends
- monthly performance trends
- top-performing products
- discount and value analysis

## Architecture

- Data generation layer: synthetic retail sales data
- Lakehouse processing: Databricks notebook example with bronze, silver, and gold layers
- Warehouse reporting: Snowflake database, table, and summary views
- Presentation layer: interactive dashboard with Streamlit

## Repository contents

- `dashboard.py` – Streamlit dashboard
- `src/retail_lakehouse/data_generator.py` – synthetic data generation
- `src/retail_lakehouse/analytics.py` – KPI and summary calculations
- `sql/snowflake_setup.sql` – Snowflake setup and reporting views
- `notebooks/databricks_lakehouse.py` – Databricks sample workflow
- `tests/test_analytics.py` – validation for analytics logic

## Run locally

```bash
cd /workspaces/SNOWFLAKE-DATABRICKS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src pytest -q
PYTHONPATH=src streamlit run dashboard.py
```

## Project name for submission
Retail Sales Analytics Lakehouse using Databricks and Snowflake

## Notes
This repository is designed to be easy to present in a final submission while remaining practical for demo and evaluation purposes.
