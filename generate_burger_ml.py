import csv
import random

random.seed(99)

bun_types = {"regular": 0, "brioche": 1, "pretzel": 2, "lettuce wrap": 3}

rows = []
for i in range(300):
    patty_count = random.choices([1, 2, 3], weights=[0.55, 0.35, 0.10])[0]
    patty_size_oz = random.choice([2, 3, 4, 6, 8])
    has_cheese = random.randint(0, 1)
    has_bacon = random.randint(0, 1)
    has_avocado = random.randint(0, 1)
    has_fried_egg = random.randint(0, 1)
    num_toppings = random.randint(1, 6)
    bun_type = random.choice(list(bun_types.keys()))
    bun_value = bun_types[bun_type]
    is_organic = random.choices([0, 1], weights=[0.75, 0.25])[0]
    restaurant_tier = random.choices([1, 2, 3], weights=[0.40, 0.40, 0.20])[0]  # 1=fast food, 2=fast casual, 3=gourmet

    # Price influenced by features
    price = (
        3.00
        + patty_count * 2.50
        + patty_size_oz * 0.40
        + has_cheese * 0.75
        + has_bacon * 1.25
        + has_avocado * 1.50
        + has_fried_egg * 1.00
        + num_toppings * 0.30
        + bun_value * 0.50
        + is_organic * 2.00
        + restaurant_tier * 1.75
        + random.gauss(0, 0.75)  # noise
    )
    price = round(max(3.00, price), 2)

    rows.append({
        "burger_id": i + 1,
        "patty_count": patty_count,
        "patty_size_oz": patty_size_oz,
        "has_cheese": has_cheese,
        "has_bacon": has_bacon,
        "has_avocado": has_avocado,
        "has_fried_egg": has_fried_egg,
        "num_toppings": num_toppings,
        "bun_type": bun_type,
        "is_organic": is_organic,
        "restaurant_tier": restaurant_tier,
        "price_usd": price,
    })

with open("burgers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

prices = [r["price_usd"] for r in rows]
print(f"Generated {len(rows)} rows")
print(f"Price range: ${min(prices):.2f} - ${max(prices):.2f}")
print(f"Avg price: ${sum(prices)/len(prices):.2f}")
