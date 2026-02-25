import csv
import random
from datetime import date, timedelta

random.seed(21)

restaurants = {
    "In-N-Out":     {"locations": ["Los Angeles, CA", "San Diego, CA", "Las Vegas, NV", "Phoenix, AZ", "Fresno, CA"], "price_range": (5, 11)},
    "Five Guys":    {"locations": ["New York, NY", "Chicago, IL", "Austin, TX", "Seattle, WA", "Denver, CO"], "price_range": (10, 18)},
    "Shake Shack":  {"locations": ["New York, NY", "Miami, FL", "Boston, MA", "Los Angeles, CA", "Chicago, IL"], "price_range": (10, 17)},
    "Whataburger":  {"locations": ["Houston, TX", "Dallas, TX", "San Antonio, TX", "Oklahoma City, OK", "Albuquerque, NM"], "price_range": (7, 14)},
    "Smashburger":  {"locations": ["Denver, CO", "Minneapolis, MN", "Nashville, TN", "Portland, OR", "Atlanta, GA"], "price_range": (9, 16)},
}

restaurant_weights = [0.30, 0.20, 0.18, 0.18, 0.14]  # In-N-Out gets most orders

burgers = {
    "In-N-Out":     ["Single", "Double-Double", "3x3", "4x4", "Animal Style", "Protein Style", "Flying Dutchman"],
    "Five Guys":    ["Little Hamburger", "Hamburger", "Little Cheeseburger", "Cheeseburger", "Bacon Burger", "Veggie Sandwich"],
    "Shake Shack":  ["ShackBurger", "SmokeShack", "Shroom Burger", "Double ShackBurger", "Cheeseburger"],
    "Whataburger":  ["Whataburger", "Double Meat", "Triple Meat", "Bacon & Cheese", "Jalapeño & Cheese", "Patty Melt"],
    "Smashburger":  ["Classic Smash", "BBQ Bacon", "Truffle Mushroom", "Spicy Baja", "Double Classic"],
}

order_types = ["Drive-Thru", "Dine-In", "Takeout", "Mobile Order"]
order_type_weights = [0.45, 0.25, 0.20, 0.10]

toppings_pool = ["Lettuce", "Tomato", "Onion", "Pickles", "Jalapeños", "Mushrooms", "Avocado", "Bacon", "Fried Egg"]

start_date = date(2023, 1, 1)
end_date = date(2025, 12, 31)
total_days = (end_date - start_date).days

rows = []
for i in range(300):
    restaurant = random.choices(list(restaurants.keys()), weights=restaurant_weights)[0]
    info = restaurants[restaurant]
    location = random.choice(info["locations"])
    city, state = location.split(", ")

    launch_date = start_date + timedelta(days=random.randint(0, total_days))
    burger = random.choice(burgers[restaurant])
    order_type = random.choices(order_types, weights=order_type_weights)[0]
    quantity = random.choices([1, 2, 3, 4], weights=[0.50, 0.30, 0.15, 0.05])[0]

    price_min, price_max = info["price_range"]
    unit_price = round(random.uniform(price_min, price_max), 2)
    total = round(unit_price * quantity, 2)

    num_toppings = random.randint(1, 5)
    toppings = ", ".join(random.sample(toppings_pool, num_toppings))

    patty_count = 1
    if any(x in burger for x in ["Double", "2x", "3x3"]):
        patty_count = 2
    elif any(x in burger for x in ["Triple", "3x", "4x4"]):
        patty_count = 3

    has_cheese = "Cheese" in burger or "ShackBurger" in burger or "Double-Double" in burger or random.random() < 0.5
    has_bacon = "Bacon" in burger or random.random() < 0.25

    wait_time_min = random.randint(2, 20)
    rating = round(random.gauss(
        {"In-N-Out": 4.6, "Five Guys": 4.2, "Shake Shack": 4.3, "Whataburger": 4.1, "Smashburger": 4.0}[restaurant],
        0.5
    ), 1)
    rating = max(1.0, min(5.0, rating))

    rows.append({
        "order_id": i + 1,
        "order_date": launch_date.strftime("%Y-%m-%d"),
        "year": launch_date.year,
        "month": launch_date.strftime("%B"),
        "quarter": f"Q{((launch_date.month - 1) // 3) + 1}",
        "day_of_week": launch_date.strftime("%A"),
        "restaurant": restaurant,
        "city": city,
        "state": state,
        "burger": burger,
        "patty_count": patty_count,
        "has_cheese": has_cheese,
        "has_bacon": has_bacon,
        "toppings": toppings,
        "order_type": order_type,
        "quantity": quantity,
        "unit_price_usd": unit_price,
        "total_usd": total,
        "wait_time_min": wait_time_min,
        "customer_rating": rating,
    })

rows.sort(key=lambda r: r["order_date"])

with open("burger_orders.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} orders")
for r in restaurants:
    count = sum(1 for row in rows if row["restaurant"] == r)
    revenue = sum(row["total_usd"] for row in rows if row["restaurant"] == r)
    avg_rating = sum(row["customer_rating"] for row in rows if row["restaurant"] == r) / count
    print(f"  {r}: {count} orders | ${revenue:,.2f} revenue | {avg_rating:.1f} avg rating")
