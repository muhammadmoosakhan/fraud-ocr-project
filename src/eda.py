import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/transactions.csv")

# Basic overview
print("📊 Dataset Info:")
print(df.info())
print("\n📈 Statistical Summary:")
print(df.describe())

# Class balance
print("\n🔢 Fraud Count:")
print(df['is_fraud'].value_counts())

# Plot fraud vs non-fraud
sns.countplot(x='is_fraud', data=df)
plt.title("Fraud vs Non-Fraud Count")
plt.xlabel("Is Fraud?")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("fraud_vs_nonfraud.png")
plt.show()

# Plot transaction amount distribution
sns.histplot(df['amount'], bins=30, kde=True)
plt.title("Transaction Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("amount_distribution.png")
plt.show()

# Optional: Geo country distribution
sns.countplot(x='geo', data=df)
plt.title("Geolocation Distribution")
plt.tight_layout()
plt.savefig("geo_distribution.png")
plt.show()
