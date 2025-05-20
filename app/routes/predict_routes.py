from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
from datetime import datetime
from app.services.feature_extractor import extract_features
from app.models import ScanHistory
from app import db

bp = Blueprint('predict', __name__)

model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')


@bp.route('/', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#     url = data.get('url')

#     if not url:
#         return jsonify({'error': 'No URL provided'}), 400

#     # Make prediction using trained model
#     features = pd.DataFrame([extract_features(url)])
#     probs = model.predict_proba(features)[0]

#     # Convert prediction number to label (e.g., 'benign')
#     proba_dict = {
#         label_encoder.classes_[i]: round(probs[i] * 100, 2)
#         for i in range(len(probs))
#     }

#     # Properly indented
#     sorted_proba = dict(
#         sorted(proba_dict.items(), key=lambda x: x[1], reverse=True))

#     # Send response back to frontend
#     return jsonify({'probabilities': sorted_proba})


def predict():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # Make prediction using trained model
        features = pd.DataFrame([extract_features(url)])
        probs = model.predict_proba(features)[0]

        # Convert prediction number to label (e.g., 'benign')
        proba_dict = {
            label_encoder.classes_[i]: round(probs[i] * 100, 2)
            for i in range(len(probs))
        }
        # Properly indented
        sorted_proba = dict(sorted(proba_dict.items(), key=lambda x: x[1], reverse=True))

        # Get result
        predicted_label = max(sorted_proba, key=sorted_proba.get)

        # Save to database
        history = ScanHistory(
            url=url,
            result=predicted_label,
            checked_at=datetime.utcnow()
        )
        db.session.add(history)
        db.session.commit()

        # Send response back to frontend  
        return jsonify({'probabilities': sorted_proba})
    except Exception as e:
        return jsonify({'error': str(e)}), 500