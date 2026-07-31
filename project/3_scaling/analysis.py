import time
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, round
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    IntegerType
)

input_path = sys.argv[1]
output_path = sys.argv[2]

spark = SparkSession.builder.appName(
    "BackblazeFailureAnalysis"
).getOrCreate()

start = time.time()

schema = StructType([
    StructField("date", StringType(), True),
    StructField("serial_number", StringType(), True),
    StructField("model", StringType(), True),
    StructField("capacity_bytes", LongType(), True),
    StructField("failure", IntegerType(), True)
])

df = (
    spark.read
    .option("header", True)
    .schema(schema)
    .csv(input_path)
)

clean_df = (
    df.filter(col("model").isNotNull())
      .filter(col("failure").isin(0, 1))
      .select("model", "failure")
      .cache()
)

row_count = clean_df.count()

result = (
    clean_df.groupBy("model")
    .agg(
        count("*").alias("drive_days"),
        sum("failure").alias("failures")
    )
    .withColumn(
        "annualized_failure_rate_pct",
        round(
            col("failures") / col("drive_days") * 36500,
            4
        )
    )
    .filter(col("drive_days") >= 100000)
    .orderBy(col("annualized_failure_rate_pct").desc())
)

result.show(20, truncate=False)

result.write.mode("overwrite").option(
    "header", True
).csv(output_path)

elapsed = time.time() - start

print("CLEANED_ROWS:", row_count)
print("ELAPSED_SECONDS:", elapsed)
print("OUTPUT_PATH:", output_path)

spark.stop()
