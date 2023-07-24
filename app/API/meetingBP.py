from flask import Blueprint, render_template, request, make_response
from app.models.meeting import Meeting
from flask import jsonify
from app import db
from flask_cors import  cross_origin


meeting_api_bp = Blueprint('meeting_api', __name__, url_prefix='/api/v1/meetings')



@meeting_api_bp.route('/', methods=['POST', 'OPTIONS'])
@cross_origin()
def create():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response
    else:
     data = request.get_json()
     new_meeting = Meeting(
        type_id=data['MeetingTypeID'],
        start_date=data['StartDate'],
        start_time=data['StartTime'],
        end_date=data['EndDate'],
        end_time=data['EndTime'],
        location=data['Location']
    )   
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting created'}), 201

@meeting_api_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Meeting.query.paginate(page=page, per_page=5)
    meetings = [meeting.to_dict() for meeting in pagination.items]
    return jsonify({
        'items': meetings,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num,
        'page': page,
        'pages': pagination.pages,  
    }), 200





@meeting_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        return jsonify(meeting.to_dict()), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        return jsonify(meeting.to_dict()), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    was_deleted = Meeting.delete(id)
    if was_deleted:
        return jsonify({'message': 'Meeting deleted'}), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404
