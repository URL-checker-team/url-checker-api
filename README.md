# 🔐 URL Threat Classification API (Flask Backend)

This is a Flask API backend that takes a URL input and uses a hybrid machine learning model to classify the URL into one of four categories:

- `benign`
- `phishing`
- `malware`
- `defacement`

---

## 🚀 Features

- Accepts POST requests with a URL
- Extracts structural features from the URL
- Uses a trained ML model (`model.pkl`) and label encoder (`label_encoder.pkl`)
- Returns a predicted label from 4 threat classes
- CORS-enabled for integration with frontend (e.g., React)

---

## 📦 Dependencies

Install required Python packages:

```bash
pip install flask flask-cors pandas joblib
```
