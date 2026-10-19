"""Daily orders aggregation batch job.

Reads raw orders and a small users dimension table, joins them, computes
per-user daily totals, and writes the result out for downstream consumption.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("daily-orders-batch").getOrCreate()

spark.conf.set("spark.sql.shuffle.partitions", "500")


def normalize_status(status):
    if status is None:
        return "unknown"
    return status.strip().lower()


normalize_status_udf = udf(normalize_status, StringType())


def run(order_date: str):
    orders = spark.read.parquet(f"s3://data/orders/dt={order_date}/")
    users = spark.read.parquet("s3://data/dim/users/")

    print("raw order count:", orders.count())

    joined = orders.join(users, orders.user_id == users.user_id)
    joined.show()
    print("joined count:", joined.count())

    joined = joined.withColumn("status_norm", normalize_status_udf(col("status")))

    deduped = joined.dropDuplicates(["order_id"])

    repartitioned = deduped.repartition(200)

    totals = repartitioned.groupBy("user_id", "status_norm").sum("amount")
    totals.cache()

    totals.write.mode("append").parquet(f"s3://data/output/daily_totals/dt={order_date}/")

    return totals


if __name__ == "__main__":
    for d in ["2026-10-14", "2026-10-15", "2026-10-16"]:
        result = run(d)
        result.cache()
        print(f"done with {d}")
