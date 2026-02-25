import csv
import random

random.seed(42)

rows = []
for i in range(200):
    crew_size = random.randint(1, 10)
    experience_score = round(random.uniform(0, 10), 1)
    fuel_level = round(random.uniform(20, 100), 1)
    equipment_quality = round(random.uniform(0, 10), 1)
    distance_km = random.randint(100, 10000)
    duration_days = random.randint(1, 60)
    communication_strength = round(random.uniform(0, 10), 1)
    weather_score = round(random.uniform(0, 10), 1)  # 10 = perfect conditions

    # Probability of success influenced by features
    score = (
        experience_score * 0.25 +
        fuel_level * 0.02 +
        equipment_quality * 0.20 +
        communication_strength * 0.15 +
        weather_score * 0.20 +
        crew_size * 0.05 -
        distance_km / 2000 -
        duration_days * 0.05
    )
    prob_success = 1 / (1 + 2.71828 ** (-score + 3))
    outcome = "success" if random.random() < prob_success else "failure"

    rows.append({
        "mission_id": i + 1,
        "crew_size": crew_size,
        "experience_score": experience_score,
        "fuel_level": fuel_level,
        "equipment_quality": equipment_quality,
        "distance_km": distance_km,
        "duration_days": duration_days,
        "communication_strength": communication_strength,
        "weather_score": weather_score,
        "outcome": outcome
    })

with open("missions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows")
successes = sum(1 for r in rows if r["outcome"] == "success")
print(f"Success: {successes}, Failure: {len(rows) - successes}")
