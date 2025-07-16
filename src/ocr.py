import cv2
import pytesseract
import json
import os
from pathlib import Path

# Configure pytesseract path (Windows)
# Uncomment below if pytesseract is not detected
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Could not read image: {img_path}")
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_fields(text):
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip() != '']

    merchant_name = lines[0] if lines else "Unknown"

    total_amount = None
    for line in lines:
        if "total" in line.lower():
            for word in line.split():
                try:
                    total_amount = float(word.replace("Rs", "").replace("$", "").replace(",", ""))
                    break
                except:
                    continue
            if total_amount:
                break

    return {
        "merchant_name": merchant_name,
        "total_amount": total_amount
    }

def process_receipts(folder_path="images"):
    result = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(folder_path, filename)
            img = preprocess_image(path)
            if img is None:
                continue
            text = pytesseract.image_to_string(img)
            fields = extract_fields(text)
            result[filename] = fields

    with open("ocr_results.json", "w") as f:
        json.dump(result, f, indent=4)
    print("✅ OCR results saved to ocr_results.json")

if __name__ == "__main__":
    process_receipts()
