
# Mini-Gateway Fraud & OCR Prototype

## Overview
This project is part of an internship assessment for building a **Fraud Detection API integrated with OCR functionality**.  
The system:
- Predicts the probability of a transaction being fraudulent based on structured data.
- Extracts merchant name and total amount from an uploaded receipt image using OCR.
- Exposes a FastAPI-based REST API with `/predict` endpoint for combined fraud detection + OCR.

---

## Tech Stack
- **Language**: Python 3.10
- **Framework**: FastAPI
- **ML Model**: XGBoost (classification for fraud detection)
- **OCR Engine**: Tesseract OCR
- **Other Tools**: Pandas, NumPy, OpenCV, Joblib
- **Containerization**: Docker

---

## Project Folder Structure
```
FRAUD-OCR-PROJECT
│
├── __pycache__/                # Compiled Python files
│   └── app.cpython-310.pyc
│
├── data/                       # Synthetic data files
│   └── transactions.csv
│
├── images/                     # Sample receipt images
│   └── sample1.jpg
│
├── src/                        # Scripts for EDA, model training, OCR
│   ├── eda.py
│   ├── generate_data.py
│   ├── model.py
│   ├── ocr.py
│   └── utils.py
│
├── venv/                       # Virtual environment
│
├── amount_distribution.png      # Visualization
├── app.py                       # Main FastAPI app
├── Dockerfile                   # Docker configuration
├── fraud_vs_nonfraud.png        # Visualization
├── geo_distribution.png          # Visualization
├── model.pkl                     # Trained fraud detection model
├── ocr_results.json              # OCR result sample
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```

---

## Setup and Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally
```bash
uvicorn app:app --reload
```
Open Swagger Docs at:
```
http://127.0.0.1:8000/docs
```

---

## Docker Setup
Build the image:
```bash
docker build -t fraud-ocr .
```
Run the container:
```bash
docker run -p 8000:8000 fraud-ocr
```
Access API:
```
http://127.0.0.1:8000/docs
```

---

## API Usage
POST `/predict`  
Fields:
- `amount` (float)
- `geo` (string)
- `BIN` (int)
- `merchant_age` (int)
- `hour` (int)
- `receipt` (image upload)

Example Response:
```json
{
  "fraud_prediction": 0,
  "fraud_probability": 0.0002,
  "merchant_name": "Walmart",
  "total_amount": 0.0
}
```

---

## Challenges & Fixes
- Virtual environment activation error → Fixed with `Set-ExecutionPolicy`
- Missing imports → Switched to correct interpreter in VSCode
- Tesseract OCR not found → Installed and configured path
- FastAPI app error → Renamed file and defined `app = FastAPI()`
- JSON serialization error → Converted `float32` to Python `float`
- Docker build delay → Waited for image to complete, used caching

---
