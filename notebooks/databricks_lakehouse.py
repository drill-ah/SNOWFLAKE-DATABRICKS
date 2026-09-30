from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("RetailLakehouseDemo").getOrCreate()

raw_df = spark.read.option("header", True).csv("/tmp/retail_sales.csv")
raw_df = raw_df.withColumn("order_date", col("order_date").cast("date"))
raw_df = raw_df.withColumn("quantity", col("quantity").cast("int"))
raw_df = raw_df.withColumn("unit_price", col("unit_price").cast("double"))
raw_df = raw_df.withColumn("discount_rate", col("discount_rate").cast("double"))
raw_df = raw_df.withColumn("revenue", col("revenue").cast("double"))

raw_df.write.mode("overwrite").format("delta").saveAsTable("retail_sales_bronze")

silver_df = raw_df.filter(col("revenue").isNotNull())
silver_df.write.mode("overwrite").format("delta").saveAsTable("retail_sales_silver")

gold_df = (
    silver_df.groupBy("category", "region")
    .sum("revenue", "quantity")
    .withColumnRenamed("sum(revenue)", "total_revenue")
    .withColumnRenamed("sum(quantity)", "total_units")
)

gold_df.write.mode("overwrite").format("delta").saveAsTable("retail_sales_gold")

spark.stop()
