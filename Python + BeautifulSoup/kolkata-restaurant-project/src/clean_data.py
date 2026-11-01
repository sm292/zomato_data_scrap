
import pandas as pd
import os

# Load raw data
input_file = "data/raw/kolkata_restaurants_raw.csv"

df = pd.read_csv(input_file)

# Remove duplicates
df.drop_duplicates(
    subset=["restaurant_name", "address"],
    inplace=True
)

# Clean restaurant names
df["restaurant_name"] = (
    df["restaurant_name"]
    .astype("string")
    .str.strip()
)

# Clean cuisine
df["cuisine"] = (
    df["cuisine"]
    .fillna("Not Available")
    .astype(str)
    .str.replace(";", ",", regex=False)
    .str.title()
)

# Clean address
df["address"] = (
    df["address"]
    .fillna("Not Available")
    .astype(str)
    .str.strip()
)

# Clean URL
df["restaurant_url"] = (
    df["restaurant_url"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Validate coordinates
df["latitude"] = pd.to_numeric(
    df["latitude"], errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"], errors="coerce"
)

# Export processed dataset
os.makedirs("data/processed", exist_ok=True)

output_file = (
    "data/processed/"
    "kolkata_restaurants_cleaned.csv"
)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Data cleaning completed!")

print("Total restaurants:", len(df))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset preview:")
print(df.head(10))

print("\nSaved:", output_file)
df.to_excel(
    "data/processed/kolkata_restaurants.xlsx",
    index=False
)