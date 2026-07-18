import time
import pandas as pd

path = "2_breaking/backblaze_2025_combined.csv"

print(f"Reading file with pandas.read_csv(): {path}")

start = time.time()

df = pd.read_csv(path)

elapsed = time.time() - start

print("Finished reading CSV")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Elapsed seconds:", elapsed)
print("Estimated pandas memory usage GB:", df.memory_usage(deep=True).sum() / 1e9)
