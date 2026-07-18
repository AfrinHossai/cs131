from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time

spark = SparkSession.builder.appName("BackblazeTopModels").getOrCreate()

input_path = "gs://double-zenith-499516-i7-cs131/backblaze_2025/*.csv"

start = time.time()

df = spark.read.option("header", True).csv(input_path)

result = (
    df.groupBy("model")
      .count()
      .orderBy(col("count").desc())
)

result.show(20, truncate=False)

elapsed = time.time() - start
print(f"Elapsed seconds: {elapsed}")

spark.stop()
