from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    from app.routes import auth_routes, predict_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(predict_routes.bp)

    with app.app_context():
        db.create_all()

    return app
