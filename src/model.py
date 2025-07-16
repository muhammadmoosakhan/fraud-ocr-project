import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_curve, auc
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib
from pathlib import Path

def train_model():
    # Load the dataset
    df = pd.read_csv("data/transactions.csv")

    # Drop columns we don't need (device_id is UUID and random)
    df = df.drop(columns=["device_id"])

    # Encode the 'geo' categorical column
    le = LabelEncoder()
    df["geo"] = le.fit_transform(df["geo"])

    # Split into features and target
    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    # Handle class imbalance
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42
    )

    # Train the model
    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)

    # Evaluate performance
    y_scores = model.predict_proba(X_test)[:, 1]
    precision, recall, _ = precision_recall_curve(y_test, y_scores)
    pr_auc = auc(recall, precision)
    print(f"✅ PR-AUC: {pr_auc:.4f}")

    # Save the model
    joblib.dump(model, "model.pkl")
    print("✅ Model saved as model.pkl")

if __name__ == "__main__":
    train_model()
