from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Secret key for JWT encoding/decoding
SECRET_KEY = 'shgldsk123jdj'

# Mock user database
USERS = {
    "test@example.com": "123456",  # Replace with hashed passwords in production
}

# Load trained model and encoder
model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# --- JWT Login Route ---


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Simple auth check (replace with secure hash in real-world)
    if USERS.get(email) == password:
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401


# === Extract features for the model ===

def extract_features(url):
    return {
        'url_length': len(url),
        'has_https': int('https' in url),
        'num_dots': url.count('.'),
        'num_digits': sum(c.isdigit() for c in url),
        'num_special_chars': sum(not c.isalnum() for c in url),
        'count_www': url.count('www'),
        'count_at': url.count('@'),
        'count_slash': url.count('/'),
        'count_dash': url.count('-')
    }


# ===  Define POST endpoint ===

@app.route('/', methods=['POST'])
def predict():
    print("✅ Received POST request")
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # Make prediction using trained model
        features = pd.DataFrame([extract_features(url)])
        pred_class = model.predict(features)[0]

        # Convert prediction number to label (e.g., 'benign')
        pred_label = label_encoder.inverse_transform([pred_class])[0]

        # Send response back to frontend
        return jsonify({
            'prediction': pred_label
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
