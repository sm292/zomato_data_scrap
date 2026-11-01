import pandas as pd

df = pd.read_csv(
    "data/processed/kolkata_restaurants_cleaned.csv"
)

print("Total records:", len(df))

print(
    "Unique restaurants:",
    df["restaurant_name"].nunique()
)

print(
    "Cuisine categories:",
    df["cuisine"].nunique()
)

print(
    "Restaurants with addresses:",
    (df["address"] != "Not Available").sum()
)

print(
    "Restaurants with URLs:",
    df["restaurant_url"].ne("").sum()
)

print(
    "Missing ratings:",
    df["ratings"].isna().sum()
)

print(
    "Missing cost:",
    df["cost_for_two"].isna().sum()
)