from datetime import datetime
import random

def run():
    # TODO: replace with real scraping.
    city_pool = ["Brussels", "Antwerp", "Gent", "Liège", "Leuven"]
    out = []
    for i in range(200):
        out.append({
            "id": f"house-{int(datetime.utcnow().timestamp())}-{i}",
            "type": "house",
            "city": random.choice(city_pool),
            "postal_code": random.choice([1000,2000,3000,4000,5000]),
            "bedrooms": random.randint(1, 6),
            "bathrooms": random.randint(1, 3),
            "land_area_m2": random.randint(80, 800),
            "living_area_m2": random.randint(60, 300),
            "price_eur": random.randint(180000, 1200000),
            "listing_date": datetime.utcnow().date().isoformat(),
        })
    return out
