from flask import Blueprint, jsonify
from app.models import ScanHistory
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import func
from app.extensions import db

bp = Blueprint("report", __name__, url_prefix="/api")


@bp.route("/report-summary", methods=["GET"])
def report_summary():
    tz = timezone("Australia/Melbourne")
    now = datetime.now(tz)
    start_date = now - timedelta(days=7)

    # base on date
    history = (
        db.session.query(
            func.date(ScanHistory.checked_at).label("date"),
            ScanHistory.result,
            func.count().label("count")
        )
        .filter(ScanHistory.checked_at >= start_date)
        .group_by(func.date(ScanHistory.checked_at), ScanHistory.result)
        .order_by("date")
        .all()
    )

    # chart data
    chart_data = {}
    for row in history:
        day = row.date.strftime("%Y-%m-%d")
        if day not in chart_data:
            chart_data[day] = {"date": day, "malicious": 0, "safe": 0}
        if row.result.lower() == "benign":
            chart_data[day]["safe"] += row.count
        else:
            chart_data[day]["malicious"] += row.count

    chart_data_list = list(chart_data.values())

    # Summary Stats
    total_count = db.session.query(
        func.count()).select_from(ScanHistory).scalar()
    malicious_count = db.session.query(func.count()).filter(
        ScanHistory.result != "benign").scalar()
    safe_count = total_count - malicious_count
    latest = db.session.query(func.max(ScanHistory.checked_at)).scalar()
    
    latest_str = latest.astimezone(tz).strftime(
        "%Y-%m-%d %H:%M") if latest else None

    return jsonify({
        "summary": {
            "totalUrlsChecked": total_count,
            "maliciousCount": malicious_count,
            "safeCount": safe_count,
            "latestCheck": latest_str
        },
        "chart": chart_data_list
    })
