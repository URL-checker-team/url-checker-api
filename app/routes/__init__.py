from .predict_routes import bp as predict_bp
from .auth_routes import bp as auth_bp
from .history_routes import bp as history_bp
from .report_routes import bp as report_bp

__all__ = ["predict_bp", "auth_bp", "history_bp", "report_bp"]

