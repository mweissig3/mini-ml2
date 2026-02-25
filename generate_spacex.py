import csv
import random
from datetime import date, timedelta

random.seed(7)

rockets = ["Falcon 9", "Falcon Heavy", "Starship"]
rocket_weights = [0.70, 0.20, 0.10]

launch_sites = {
    "Falcon 9":     ["Cape Canaveral SLC-40", "Vandenberg SLC-4E", "Kennedy LC-39A"],
    "Falcon Heavy": ["Kennedy LC-39A"],
    "Starship":     ["Starbase, TX"],
}

orbits = {
    "Falcon 9":     ["LEO", "GTO", "ISS", "SSO", "Polar", "MEO"],
    "Falcon Heavy": ["GTO", "HEO", "Heliocentric"],
    "Starship":     ["LEO", "TLI", "TMI"],
}

customers = ["NASA", "SpaceX (Starlink)", "DoD", "Commercial Satellite Co.",
             "ESA", "Axiom Space", "Planet Labs", "Iridium"]

rocket_payload = {
    "Falcon 9":     (2000, 22800),
    "Falcon Heavy": (8000, 63800),
    "Starship":     (50000, 150000),
}

rocket_cost = {
    "Falcon 9":     (62, 80),
    "Falcon Heavy": (90, 150),
    "Starship":     (10, 30),  # projected low-cost
}

# Success rates by rocket (mature -> high, Starship -> lower)
success_rate = {
    "Falcon 9":     0.95,
    "Falcon Heavy": 0.90,
    "Starship":     0.65,
}

booster_landing_rate = {
    "Falcon 9":     0.90,
    "Falcon Heavy": 0.80,
    "Starship":     0.60,
}

start_date = date(2020, 1, 1)
end_date = date(2025, 12, 31)
total_days = (end_date - start_date).days

rows = []
flight_counters = {"Falcon 9": 0, "Falcon Heavy": 0, "Starship": 0}
booster_reuse = {}  # booster_id -> reuse_count

for i in range(180):
    rocket = random.choices(rockets, weights=rocket_weights)[0]
    flight_counters[rocket] += 1

    launch_date = start_date + timedelta(days=random.randint(0, total_days))
    site = random.choice(launch_sites[rocket])
    orbit = random.choice(orbits[rocket])
    customer = random.choice(customers)

    payload_min, payload_max = rocket_payload[rocket]
    payload_kg = random.randint(payload_min, payload_max)

    cost_min, cost_max = rocket_cost[rocket]
    cost_usd_million = round(random.uniform(cost_min, cost_max), 1)

    # Booster reuse
    booster_id = f"B{1050 + (i % 12)}"
    reuse_count = booster_reuse.get(booster_id, 0)
    booster_reuse[booster_id] = reuse_count + 1

    outcome = "Success" if random.random() < success_rate[rocket] else "Failure"

    can_land = rocket != "Starship" or True  # all attempt landing
    if outcome == "Success":
        landed = "Success" if random.random() < booster_landing_rate[rocket] else "Failure"
    else:
        landed = "Failure"

    duration_min = random.randint(1, 10)

    rows.append({
        "launch_id": i + 1,
        "launch_date": launch_date.strftime("%Y-%m-%d"),
        "year": launch_date.year,
        "month": launch_date.strftime("%B"),
        "quarter": f"Q{((launch_date.month - 1) // 3) + 1}",
        "rocket": rocket,
        "flight_number": flight_counters[rocket],
        "booster_id": booster_id,
        "booster_reuse_count": reuse_count,
        "launch_site": site,
        "orbit": orbit,
        "customer": customer,
        "payload_kg": payload_kg,
        "cost_usd_million": cost_usd_million,
        "mission_duration_min": duration_min,
        "outcome": outcome,
        "booster_landing": landed,
    })

# Sort by date
rows.sort(key=lambda r: r["launch_date"])

with open("spacex_launches.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} launches")
for r in rockets:
    count = sum(1 for row in rows if row["rocket"] == r)
    wins = sum(1 for row in rows if row["rocket"] == r and row["outcome"] == "Success")
    print(f"  {r}: {count} launches, {wins} successes ({100*wins//count}%)")
