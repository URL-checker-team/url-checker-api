from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import VotingClassifier
from app.services.feature_extractor import extract_features
from app.models import DatasetFile
from datetime import datetime
from app.extensions import db


# Define Flask blueprint for training-related endpoints
bp = Blueprint("train", __name__, url_prefix="/api")

# Ensure upload and model directories exist


def ensure_directories():
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(current_app.config['MODEL_FOLDER'], exist_ok=True)

# === Route: Upload CSV Dataset ===


@bp.route("/upload-dataset", methods=["POST"])
def upload_dataset():

    # Validate file part
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files allowed"}), 400

    # Save uploaded file to the configured upload folder
    filename = file.filename
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(upload_path)

    # ✅ save upload record to database
    new_record = DatasetFile(filename=filename, uploaded_at=datetime.utcnow())
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "File uploaded", "filename": filename})


# === Route: Train Model using uploaded dataset ===
@bp.route("/train-model", methods=["POST"])
def train_model():
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    csv_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if not os.path.exists(csv_path):
        return jsonify({"error": "File not found"}), 404

    try:
        # Load dataset
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=["url"])

        # Encode target labels
        label_encoder = LabelEncoder()
        df["type"] = label_encoder.fit_transform(df["type"])

        # Extract features from URLs
        feature_df = df["url"].apply(lambda x: pd.Series(extract_features(x)))
        X = feature_df
        y = df["type"]

        # Split into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=y, test_size=0.2, random_state=42
        )

        # Define individual models
        # n_estimators：The number of decision trees，random_state：Sets the random seed for reproducibility.
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        # objective='multi:softmax'：Sets the learning task to multi-class classification
        # num_class=len(le.classes_)：Specifies the number of target classes (e.g., benign, malware, phishing).
        # eval_metric='mlogloss'：This sets the evaluation metric during training to multiclass log loss
        xgb = XGBClassifier(objective="multi:softmax",
                            num_class=len(label_encoder.classes_))

        # Define ensemble model using soft voting
        model = VotingClassifier(
            estimators=[("rf", rf), ("xgb", xgb)], voting="soft")
        model.fit(X_train, y_train)

        # Save the trained model and label encoder to disk
        model_path = os.path.join(
            current_app.config["MODEL_FOLDER"], "model.pkl")
        le_path = os.path.join(
            current_app.config["MODEL_FOLDER"], "label_encoder.pkl")
        joblib.dump(model, model_path)
        joblib.dump(label_encoder, le_path)

        return jsonify({"message": "Model trained and saved."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Route: check upload history route ===
@bp.route("/upload-history", methods=["GET"])
def upload_history():
    records = DatasetFile.query.order_by(
        DatasetFile.uploaded_at.desc()).limit(10).all()
    result = [
        {
            "filename": r.filename,
            "uploadedAt": r.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in records
    ]
    return jsonify(result)
