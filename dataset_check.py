import pandas as pd

file_path = "data/raw/power_grid.csv"

df = pd.read_csv(file_path)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- UNIQUE TRANSFORMERS ---")
print(df["transformer_id"].unique())

print("\n--- UNIQUE FEEDERS ---")
print(df["feeder_id"].unique())

print("\n--- TIME RANGE ---")
print(df["timestamp"].min())
print(df["timestamp"].max())

output_path = "data/processed/power_grid_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nCleaned dataset saved to: {output_path}")
