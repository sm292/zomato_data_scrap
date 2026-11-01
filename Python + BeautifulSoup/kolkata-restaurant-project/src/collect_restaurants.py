
import requests
import pandas as pd
import os
import time
from datetime import datetime, timezone

# =====================================
# CONFIGURATION
# =====================================

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Approximate Kolkata bounding box
SOUTH, WEST = 22.35, 88.15
NORTH, EAST = 22.75, 88.55

MAX_RECORDS = 1000

# =====================================
# OVERPASS QUERY
# =====================================

query = f"""
[out:json][timeout:180];

(
  node["amenity"="restaurant"]
    ({SOUTH},{WEST},{NORTH},{EAST});

  way["amenity"="restaurant"]
    ({SOUTH},{WEST},{NORTH},{EAST});

  relation["amenity"="restaurant"]
    ({SOUTH},{WEST},{NORTH},{EAST});
);

out center tags;
"""

headers = {
    "User-Agent": (
        "KolkataRestaurantResearch/1.0 "
        "(independent educational project)"
    )
}

# =====================================
# FETCH DATA WITH LIMITED RETRIES
# =====================================

print("Fetching Kolkata restaurant data...")

response = None

for attempt in range(3):

    try:
        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=headers,
            timeout=240
        )

        if response.status_code in (429, 503):
            print("Server busy. Waiting before retry...")
            time.sleep(30)
            continue

        response.raise_for_status()
        break

    except requests.RequestException as error:

        if attempt == 2:
            raise RuntimeError(
                f"Data collection failed: {error}"
            )

        time.sleep(10)

if response is None or not response.ok:
    raise RuntimeError("Overpass API is currently unavailable.")

data = response.json()

elements = data.get("elements", [])

print("Raw records retrieved:", len(elements))

# =====================================
# EXTRACT RESTAURANT INFORMATION
# =====================================

records = []

def extract_address(tags):

    if tags.get("addr:full"):
        return tags["addr:full"]

    fields = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:city"),
        tags.get("addr:postcode")
    ]

    return ", ".join(
        str(value) for value in fields if value
    )


for item in elements:

    tags = item.get("tags", {})

    restaurant_name = tags.get("name")

    if not restaurant_name:
        continue

    # Coordinates
    if item["type"] == "node":

        lat = item.get("lat")
        lon = item.get("lon")

    else:

        center = item.get("center", {})

        lat = center.get("lat")
        lon = center.get("lon")

    # Cuisine
    cuisine = tags.get("cuisine", "")

    # Official website
    restaurant_url = (
        tags.get("website")
        or tags.get("contact:website")
        or ""
    )

    records.append({

        "restaurant_name": restaurant_name,

        "cuisine": cuisine,

        "ratings": None,

        "cost_for_two": None,

        "address": extract_address(tags),

        "restaurant_url": restaurant_url,

        "osm_id": f"{item['type']}/{item['id']}",

        "osm_record_url": (
            f"https://www.openstreetmap.org/"
            f"{item['type']}/{item['id']}"
        ),

        "latitude": lat,

        "longitude": lon,

        "source": "OpenStreetMap",

        "collected_at": datetime.now(
            timezone.utc
        ).isoformat()

    })

# =====================================
# CREATE DATAFRAME
# =====================================

df = pd.DataFrame(records)

if df.empty:
    raise ValueError("No named restaurants found.")

df.drop_duplicates(
    subset=["osm_id"],
    inplace=True
)

df.drop_duplicates(
    subset=["restaurant_name", "address"],
    inplace=True
)

df = df.head(MAX_RECORDS)

# =====================================
# EXPORT RAW CSV
# =====================================

output_file = (
    "data/raw/kolkata_restaurants_raw.csv"
)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nCollection completed!")
print("Restaurants:", len(df))
print("File:", output_file)

print("\nPreview:")
print(df.head(10))
