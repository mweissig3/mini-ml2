import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import math

# Load data
df = pd.read_csv("burgers.csv")

# One-hot encode bun_type
df = pd.get_dummies(df, columns=["bun_type"])

X = df.drop(columns=["burger_id", "price_usd"])
y = df["price_usd"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = math.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE:  ${mae:.2f}")
print(f"RMSE: ${rmse:.2f}")
print(f"R²:   {r2:.4f}")

# Feature importance
feature_names = df.drop(columns=["burger_id", "price_usd"]).columns
coefficients = pd.Series(model.coef_, index=feature_names).sort_values(ascending=False)
print("\nFeature Coefficients (impact on price):")
print(coefficients.to_string())
