from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db

from app.routes import predict_bp, auth_bp, history_bp, report_bp, train_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from app import models

    app.register_blueprint(predict_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(train_bp)

    with app.app_context():
        db.create_all()

    return app
