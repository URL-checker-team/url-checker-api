## 📦 Model Setup

🔒 The trained model files are not included in this repository due to GitHub's file size restrictions and security considerations.

Please download the following files from our shared drive:

👉 Download model files here：
https://liveswinburneeduau-my.sharepoint.com/:f:/r/personal/104725051_student_swin_edu_au/Documents/url-checker-api?csf=1&web=1&e=ePqotC

Required files:

model.pkl – Trained machine learning model

label_encoder.pkl – Label encoder for decoding prediction outputs

Once downloaded, place both files into the root of the url-checker-api/ directory like so:

url-checker-api/
│
├── app/
│   ├── __init__.py              
│   ├── models.py                
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py       
│   │   ├── predict_routes.py    
│   │   └── train_routes.py      
│   ├── services/
│   │   ├── jwt_utils.py         
│   │   └── feature_extractor.py
│   └── uploads/                
│
├── config.py                    
├── run.py                       
├── model.pkl                    
├── label_encoder.pkl            
└── requirements.txt


The backend will fail to start or make predictions if these files are missing.

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
pip install flask flask-cors pandas joblib PyJWT
pip install flask flask-cors flask-sqlalchemy pymysql werkzeug pyjwt

```

## Start the Flask server

In the terminal:

python run.py

If successful, you’ll see output like:

- Running on http://127.0.0.1:5050/ (Press CTRL+C to quit)


## create tables in database

```bash
python create_admin.py   
