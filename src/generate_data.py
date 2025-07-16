import pandas as pd
import numpy as np
import uuid
import random
from pathlib import Path

def generate_synthetic_data(n_legit=9990, n_fraud=10, seed=42):
    np.random.seed(seed)
    data = []

    def random_bin():
        return random.choice([411111, 550000, 601100, 300000, 123456])

    def random_geo():
        return random.choice(["PK", "IN", "US", "AE", "BD", "NG"])

    for i in range(n_legit + n_fraud):
        is_fraud = 1 if i < n_fraud else 0
        amount = np.random.uniform(10, 5000) if not is_fraud else np.random.choice([5, 9999])
        device_id = str(uuid.uuid4())
        geo = random_geo()
        BIN = random_bin()
        merchant_age = np.random.randint(0, 365)
        hour = np.random.randint(0, 24)

        data.append([amount, device_id, geo, BIN, merchant_age, hour, is_fraud])

    df = pd.DataFrame(data, columns=[
        "amount", "device_id", "geo", "BIN", "merchant_age", "hour", "is_fraud"
    ])

    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/transactions.csv", index=False)
    print("✅ transactions.csv created with", len(df), "rows.")

if __name__ == "__main__":
    generate_synthetic_data()
