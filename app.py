from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
import pytesseract
import cv2
import numpy as np

# ✅ Create FastAPI app
app = FastAPI(title="Fraud Detection & OCR API")

# ✅ Load model safely
try:
    model = joblib.load("model.pkl")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# ✅ OCR config
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Preprocess image for OCR
def preprocess_image(image_bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

# ✅ Extract merchant name and total from text
def extract_fields(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    merchant_name = lines[0] if lines else "Unknown"

    total_amount = None
    for line in lines:
        if "total" in line.lower():
            for word in line.split():
                try:
                    total_amount = float(word.replace("Rs", "").replace("$", "").replace(",", "").replace(":", ""))
                    break
                except:
                    continue
            if total_amount:
                break

    return {
        "merchant_name": merchant_name,
        "total_amount": total_amount or 0.0
    }

# ✅ Root route for testing
@app.get("/")
def home():
    return {"status": "API is running!"}

# ✅ Main prediction endpoint
@app.post("/predict")
async def predict(
    amount: float = Form(...),
    geo: str = Form(...),
    BIN: int = Form(...),
    merchant_age: int = Form(...),
    hour: int = Form(...),
    receipt: UploadFile = File(...)
):
    # Fraud prediction
    if model is None:
        return JSONResponse({"error": "Model not loaded"}, status_code=500)

    input_df = pd.DataFrame([{
        "amount": amount,
        "geo": geo,
        "BIN": BIN,
        "merchant_age": merchant_age,
        "hour": hour
    }])

    # Encode geo
    geo_map = {"PK": 0, "IN": 1, "US": 2, "AE": 3, "BD": 4, "NG": 5}
    input_df["geo"] = input_df["geo"].map(geo_map).fillna(0).astype(int)

    prob = float(model.predict_proba(input_df)[0][1])  # ✅ Convert to Python float
    pred = int(prob > 0.5)


    # OCR
    image_bytes = await receipt.read()
    image = preprocess_image(image_bytes)
    text = pytesseract.image_to_string(image)
    ocr_result = extract_fields(text)

    return JSONResponse({
    "fraud_prediction": pred,
    "fraud_probability": round(prob, 4),
    "merchant_name": ocr_result["merchant_name"],
    "total_amount": float(ocr_result["total_amount"])
})

