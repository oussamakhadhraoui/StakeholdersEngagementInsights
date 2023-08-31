from flask import Blueprint, jsonify, request
from app.models.attendance import Attendance
from app.models.person import Person
from app.models.meeting import Meeting
from app import db
import datetime

attendance_api_bp = Blueprint('attendance_api', __name__, url_prefix='/api/v1/attendances')

@attendance_api_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
     # Fetch the PersonID using the email
    person = Person.get_by_email(data['email']) # assuming email is passed in data
    if not person:
        return jsonify({'message': 'Person not found'}), 404
    
    # Fetch the MeetingID using the title
    meeting = Meeting.get_by_title(data['title']) # assuming title is passed in data
    if not meeting:
        return jsonify({'message': 'Meeting not found'}), 404
    
    attendance_duration = data.get('attendance_duration')
    if attendance_duration:
        attendance_duration = datetime.datetime.strptime(attendance_duration, '%I:%M %p').time()

    new_attendance = Attendance(
        person_id=data['PersonID'],
        meeting_id=data['MeetingID'],
        attendance_duration=attendance_duration
    )

    db.session.add(new_attendance)
    db.session.commit()
    return jsonify(new_attendance.to_dict()), 201

@attendance_api_bp.route('/', methods=['GET'])
def index():
    attendances = Attendance.query.all()
    return jsonify({'items': [attendance.to_dict() for attendance in attendances]}), 200

@attendance_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    attendance = Attendance.get_by_id(id)
    if attendance:
        return jsonify(attendance.to_dict()), 200
    else:
        return jsonify({'message': 'Attendance not found'}), 404

@attendance_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    attendance = Attendance.get_by_id(id)
    if attendance:
        attendance_duration = data.get('attendance_duration')
        if attendance_duration:
            attendance_duration = datetime.datetime.strptime(attendance_duration, '%I:%M %p').time()

        attendance.update({
            'person_id': data.get('PersonID'),
            'meeting_id': data.get('MeetingID'),
            'attendance_duration': attendance_duration
        })
        
        db.session.commit()
        return jsonify(attendance.to_dict()), 200
    else:
        return jsonify({'message': 'Attendance not found'}), 404

@attendance_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    success = Attendance.delete(id)
    if success:
        return jsonify({'message': 'Attendance deleted'}), 200
    else:
        return jsonify({'message': 'Attendance not found'}), 404
