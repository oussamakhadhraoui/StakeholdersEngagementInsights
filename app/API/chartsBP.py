from flask import Blueprint, jsonify, request
from app import db
from sqlalchemy import text
from app.queries import BAR_CHART_1, MAP_CHART_1, BAR_CHART_2, CARD_CHART

charts_api_bp = Blueprint('charts_api', __name__, url_prefix='/api/v1/charts')

@charts_api_bp.route('/<int:chart_id>', methods=['GET'])
def chart_data(chart_id):
    meeting_type_id = request.args.get('meetingType')
    time_interval = request.args.get('timeInterval', 'daily')  # Default to 'daily' if not provided
    meeting_id = request.args.get('meetingId')

    chart_type = None
    result_proxy = None

    if chart_id == 1:  
        chart_type = "bar"
        result_proxy = db.session.execute(text(BAR_CHART_1), {"meeting_type_id": meeting_type_id, "time_interval": time_interval})
    
    elif chart_id == 2:
        chart_type = "map"
        result_proxy = db.session.execute(text(MAP_CHART_1), {"meeting_type_id": meeting_type_id})
        
    elif chart_id == 3:  
        chart_type = "stackedColumn"
        result_proxy = db.session.execute(text(BAR_CHART_2), {"meeting_id": meeting_id})

    elif chart_id == 4:
        chart_type = "card"
        result_proxy = db.session.execute(text(CARD_CHART), {"meeting_id": meeting_id})
        row = {column: value for column, value in zip(result_proxy.keys(), result_proxy.fetchone())}
        row["PresencePercentage"] = float(row["PresencePercentage"])
        data = {
            "chartType": chart_type,
            "data": {
                "TotalAbsent": row["TotalAbsent"],
                "TotalAttended": row["TotalAttended"],
                "UniqueAffiliations": row["UniqueAffiliations"],
                "PresencePercentage": row["PresencePercentage"]
            }
        }
        return jsonify(data)

    # Convert the result into a format suitable for your frontend charting library
    columns = result_proxy.keys() if result_proxy else []
    data = {
        "chartType": chart_type,
        "data": [dict(zip(columns, row)) for row in result_proxy] if result_proxy else None
    }

    # Convert datetime.date and Decimal before sending the data
    for item in data['data']:
        if 'Date' in item:
            item['Date'] = item['Date'].strftime('%Y-%m-%d')  # Convert date to string
        if 'participants' in item:
            item['participants'] = float(item['participants'])  # Convert Decimal to float
        
    return jsonify(data)