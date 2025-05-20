from flask import Blueprint, jsonify
from app.models import ScanHistory

bp = Blueprint('history', __name__)

@bp.route('/history', methods=['GET'])
def get_history():
    records = ScanHistory.query.order_by(ScanHistory.checked_at.desc()).limit(100).all()
    result = [
        {
            'url': r.url,
            'result': r.result,
            'checkedAt': r.checked_at.strftime("%Y-%m-%d %H:%M")
        }
        for r in records
    ]
    return jsonify(result)
