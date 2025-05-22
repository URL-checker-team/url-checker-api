import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask secret key
    SECRET_KEY = 'shgldsk123jdj'

    # MySQL database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19901110355Wj-yh@localhost/urldb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload & model save paths
    UPLOAD_FOLDER = os.path.join(basedir, "app", "uploads")  # ← uploaded CSVs
    MODEL_FOLDER = os.path.join(basedir, "models")           # ← model.pkl etc.

    # Restrict file uploads
    ALLOWED_EXTENSIONS = {"csv"}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
