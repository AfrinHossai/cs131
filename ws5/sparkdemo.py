from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ws5-regression").getOrCreate()
import sys
input_path = sys.argv[1]

data = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)

data.show()
from pyspark.ml.feature import VectorAssembler
assembler = VectorAssembler(
    inputCols=["total_bill", "size"],
    outputCol="features"
)
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import LinearRegression
# A4: Split the data reproducibly
train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)


# A5: Define the regression model and pipeline
regression = LinearRegression(
    featuresCol="features",
    labelCol="tip"
)

pipeline = Pipeline(stages=[assembler, regression])
pipeline_model = pipeline.fit(train_data)


# A6: Generate predictions
predictions = pipeline_model.transform(test_data)


# A7: Evaluate RMSE and R-squared
evaluator = RegressionEvaluator(
    labelCol="tip",
    predictionCol="prediction"
)

rmse = evaluator.setMetricName("rmse").evaluate(predictions)
r2 = evaluator.setMetricName("r2").evaluate(predictions)


# A8: Print model information and evaluation metrics
linear_model = pipeline_model.stages[-1]

print(f"Coefficients: {linear_model.coefficients}")
print(f"Intercept: {linear_model.intercept}")
print(f"RMSE: {rmse}")
print(f"R-squared: {r2}")


spark.stop()

