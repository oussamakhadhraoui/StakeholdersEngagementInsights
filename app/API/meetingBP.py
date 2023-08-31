from flask import Blueprint, request
from app.models.meeting import Meeting
from app.models.meetingtype import MeetingType
from flask import jsonify
from app import db


meeting_api_bp = Blueprint('meeting_api', __name__, url_prefix='/api/v1/meetings')

@meeting_api_bp.route('/', methods=['POST', 'OPTIONS'])
def create():
        data = request.get_json()
        new_meeting = Meeting(
            type_id=data['MeetingTypeID'],
            start_date=data['StartDate'],
            start_time=data['StartTime'],
            end_date=data['EndDate'],
            end_time=data['EndTime'],
            location=data['Location'],
            title=data['Title']  
        )   
        db.session.add(new_meeting)
        db.session.commit()
        return jsonify({'message': 'Meeting created'}), 201



@meeting_api_bp.route('/', methods=['GET'])
def index():
    meetings = Meeting.query.all()
    return jsonify({'items': [meeting.to_dict() for meeting in meetings]}), 200

@meeting_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        return jsonify(meeting.to_dict()), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    meeting = Meeting.get_by_id(id)
    if meeting:
        meeting.update({
            'type_id': data.get('MeetingTypeID'),
            'start_date': data.get('StartDate'),
            'start_time': data.get('StartTime'),
            'end_date': data.get('EndDate'),
            'end_time': data.get('EndTime'),
            'location': data.get('Location'),
            'title': data.get('Title'),  
        })
        db.session.commit()
        return jsonify({'message': 'Meeting updated'}), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404

@meeting_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    meeting = Meeting.get_by_id(id)
    if meeting:
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({'message': 'Meeting deleted'}), 200
    else:
        return jsonify({'message': 'Meeting not found'}), 404
    
