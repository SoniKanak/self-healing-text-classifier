# 🧠 Self-Healing Text Classification API

This project implements a **self-healing sentiment classification system** that:
1. Takes text input (e.g., product or movie reviews)
2. Classifies the sentiment (Positive/Negative)
3. Checks model confidence
4. Applies a fallback rule-based strategy if the model is uncertain

It exposes a REST API using FastAPI and logs every prediction for traceability.

---

## ✨ Features

- Custom rule-based sentiment classification
- Confidence-based prediction filtering
- Fallback strategy using keyword matching
- RESTful API interface using FastAPI
- Logging of every prediction to a file
- Postman/Python-compatible for testing
- Lightweight, runs entirely offline

---

## 📦 Installation

Clone this repository or download the project folder.

Then run:

```bash
pip install -r requirements.txt

🚀 Running the API
Start the server:
python run_api.py
This will launch the server on:
http://127.0.0.1:8001
📮 API Endpoint
POST /classify
Used to classify sentiment of the given text.

🔹 Request Body:
json
{
  "text": "I really loved this movie!"
}
🔹 Response:
json
{
  "prediction": "Positive",
  "confidence": 85.6,
  "used_fallback": false
}
🧪 Testing the API
➤ Using Postman:
Method: POST

URL: http://127.0.0.1:8001/classify

Headers:

Content-Type: application/json

Body:

json
{
  "text": "The experience was disappointing."
}
➤ Using Python:
Create a file api_test.py:

python
import requests
import json

url = "http://127.0.0.1:8001/classify"
data = {"text": "I hated the product!"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2))
Run it:

bash
python api_test.py
🧾 Logs
All API responses are logged in the logs/ folder.

Example:

bash
logs/log_20240620_153142.txt
Contents:

yaml
Timestamp: 2024-06-20 15:31:42
Input: The product was okay
Prediction: Negative
Confidence: 65.0
Used Fallback: True
🧠 Classifier Logic Summary
The classifier checks for sentiment words in input text.

It calculates a confidence score based on match weights.

If the score is below threshold (default: 0.7), it:

Triggers a fallback rule

Returns a prediction with used_fallback = true

📂 Project Structure
Self-Healing-Text-Classification/
├── classifier_api.py         # FastAPI app
├── run_api.py                # Launch server
├── text_classifier.py        # Main classifier logic
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── logs/                     # Logs folder (auto-generated)
├── api_test.py               # Optional API test script
└── example.py                # Optional CLI example

📜 License
This project is for academic use only, developed under the AI Internship Project.

