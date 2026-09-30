-- Snowflake setup for Retail Sales Analytics Lakehouse
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE DATABASE RETAIL_LAKEHOUSE;
CREATE OR REPLACE SCHEMA RETAIL_LAKEHOUSE.PUBLIC;

CREATE OR REPLACE TABLE RETAIL_LAKEHOUSE.PUBLIC.RAW_SALES (
    order_id STRING,
    order_date DATE,
    store STRING,
    region STRING,
    category STRING,
    product STRING,
    quantity NUMBER(18,0),
    unit_price NUMBER(18,2),
    discount_rate NUMBER(18,4),
    revenue NUMBER(18,2),
    orders NUMBER(18,0)
);

CREATE OR REPLACE VIEW RETAIL_LAKEHOUSE.PUBLIC.VW_SALES_SUMMARY AS
SELECT
    category,
    region,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units
FROM RETAIL_LAKEHOUSE.PUBLIC.RAW_SALES
GROUP BY category, region;

CREATE OR REPLACE MATERIALIZED VIEW RETAIL_LAKEHOUSE.PUBLIC.MV_MONTHLY_REVENUE AS
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(revenue) AS revenue,
    COUNT(DISTINCT order_id) AS orders
FROM RETAIL_LAKEHOUSE.PUBLIC.RAW_SALES
GROUP BY TO_CHAR(order_date, 'YYYY-MM');
