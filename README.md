# Mini-Gateway Fraud & OCR Prototype

## Overview
This project is part of an internship assessment at **Karsaz Solutions**.  
The goal was to build a **Fraud Detection API integrated with OCR functionality**:

✔ Predicts the probability of a transaction being fraudulent based on structured transaction data.  
✔ Extracts merchant name and total amount from an uploaded receipt image using OCR.  
✔ Exposes a **FastAPI-based REST API** with `/predict` endpoint for combined fraud detection + OCR.  
✔ Fully containerized using **Docker** for deployment.  

---

## Tech Stack
- **Language:** Python 3.10  
- **Framework:** FastAPI  
- **Machine Learning:** XGBoost (fraud classification)  
- **OCR Engine:** Tesseract OCR  
- **Other Tools:** Pandas, NumPy, OpenCV, Joblib  
- **Containerization:** Docker  

---

## Project Structure
```
FRAUD-OCR-PROJECT
│
├── data/                       # Synthetic dataset
│   └── transactions.csv
│
├── images/                     # Sample receipt images
│   └── sample1.jpg
│
├── src/                        # Supporting scripts
│   ├── eda.py                  # Exploratory Data Analysis
│   ├── generate_data.py        # Synthetic data generation
│   ├── model.py                # Fraud model training
│   ├── ocr.py                  # OCR extraction logic
│   └── utils.py
│
├── amount_distribution.png     # Visualization
├── fraud_vs_nonfraud.png       # Visualization
├── geo_distribution.png        # Visualization
│
├── app.py                      # Main FastAPI application
├── Dockerfile                  # Docker configuration
├── model.pkl                   # Trained fraud detection model
├── ocr_results.json            # Sample OCR output
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
└── venv/                       # Virtual environment (unused finally)
```

---

## ✅ Setup & Installation (Local)

### 1. Virtual Environment (Attempted but faced issues)
Initially tried:
```bash
python -m venv venv
venv\Scripts\activate
```
**Issue:** PowerShell Execution Policy error → Fixed by:
```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
**Still faced interpreter issues in VS Code → Switched to global interpreter and proceeded without venv.**

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Run Locally
```bash
uvicorn app:app --reload
```
Open Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## ✅ Docker Setup

### 1. Enable Virtualization
- Enter **BIOS** → Enable **Intel Virtualization Technology (VT-x)**  
- (Not VT-d, as that is for I/O virtualization)  
- Restart PC → Confirm in **Task Manager → Performance → Virtualization: Enabled**  

---

### 2. Build Docker Image
```bash
docker build --no-cache -t fraud-ocr . --progress=plain
```

---

### 3. Run Docker Container
```bash
docker run -p 8000:8000 fraud-ocr
```

Expected Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Access API:
```
http://127.0.0.1:8000/docs
```

---

### 4. Push to Docker Hub
```bash
docker tag fraud-ocr <your-dockerhub-username>/fraud-ocr:latest
docker push <your-dockerhub-username>/fraud-ocr:latest
```

---

## ✅ API Usage

**POST** `/predict`  
Fields:
- `amount` (float)
- `geo` (string)
- `BIN` (int)
- `merchant_age` (int)
- `hour` (int)
- `receipt` (image upload)

Sample Response:
```json
{
  "fraud_prediction": 0,
  "fraud_probability": 0.0002,
  "merchant_name": "Walmart",
  "total_amount": 0.0
}
```

---

## ✅ GitHub Push Steps
1. Initialize and set remote:
```bash
git init
git remote set-url origin https://github.com/muhammadmoosakhan/fraud-ocr-project.git
```

2. Push Code:
```bash
git add .
git commit -m "Initial commit - Fraud OCR Project"
git push -u origin main
```

---

## ✅ Challenges & Fixes

### 1. Virtual Environment Issues
- **Problem:** Activation blocked by PowerShell policy  
- **Fix:**  
  ```bash
  Set-ExecutionPolicy RemoteSigned
  ```
- **Decision:** Interpreter issues persisted → Switched to global Python interpreter

---

### 2. OCR (Tesseract) Not Found
- **Problem:** `pytesseract.pytesseract.TesseractNotFoundError`  
- **Fix:** Installed Tesseract manually, added to PATH:
```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

### 3. FastAPI App Error
- **Problem:** Attribute `"app"` not found in module  
- **Fix:** Renamed main script to **app.py** and added:
```python
app = FastAPI()
```

---

### 4. JSON Serialization Error
- **Problem:** `TypeError: Object of type float32 is not JSON serializable`  
- **Fix:** Converted NumPy float to Python float:
```python
"fraud_probability": float(prob),
"total_amount": float(ocr_result["total_amount"])
```

---

### 5. Docker Issues
- **Problem 1:** Dockerfile empty  
  **Fix:** Added complete Dockerfile with proper commands  
- **Problem 2:** `uvicorn not found in $PATH`  
  **Fix:** Added `uvicorn` in `requirements.txt` and CMD:
```dockerfile
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
- **Problem 3:** Virtualization not enabled → Fixed in BIOS by enabling Intel VT-x  

---

## ✅ Key Learnings
✔ Setting up **FastAPI** with ML + OCR  
✔ Handling **interpreter and PATH issues** in Windows  
✔ Configuring **Docker with Tesseract OCR** support  
✔ Debugging **JSON serialization** and runtime errors  
✔ BIOS-level **virtualization setup** for Docker Desktop  

---
