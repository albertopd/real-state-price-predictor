from datetime import datetime
import random

def run():
    # TODO: replace with real scraping.
    # This is a stub that returns a list of dicts.
    city_pool = ["Brussels", "Antwerp", "Gent", "Liège", "Leuven"]
    out = []
    for i in range(200):
        out.append({
            "id": f"apt-{int(datetime.utcnow().timestamp())}-{i}",
            "type": "apartment",
            "city": random.choice(city_pool),
            "postal_code": random.choice([1000,2000,3000,4000,5000]),
            "bedrooms": random.randint(0, 4),
            "bathrooms": random.randint(1, 2),
            "living_area_m2": random.randint(30, 160),
            "price_eur": random.randint(120000, 650000),
            "listing_date": datetime.utcnow().date().isoformat(),
        })
    return out
