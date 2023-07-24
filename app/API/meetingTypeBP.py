from flask import Blueprint, jsonify, request
from app.models.meetingtype import MeetingType
from app import db

meetingType_api_bp = Blueprint('meetingType_api', __name__, url_prefix='/api/v1/meeting-types')

@meetingType_api_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    new_type = MeetingType(
        type=data['type']
    )
    db.session.add(new_type)
    db.session.commit()
    return jsonify(new_type.to_dict()), 201

@meetingType_api_bp.route('/', methods=['GET'])
def index():
    types = MeetingType.query.all()
    return jsonify([type.to_dict() for type in types]), 200

@meetingType_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    type = MeetingType.get_by_id(id)
    if type:
        return jsonify(type.to_dict()), 200
    else:
        return jsonify({'message': 'MeetingType not found'}), 404

@meetingType_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    type = MeetingType.get_by_id(id)
    if type:
        type.update({
            'id': data.get('MeetingTypeID'),
            'type': data.get('Type'),
        })
        db.session.commit()
        return jsonify(type.to_dict()), 200
    else:
        return jsonify({'message': 'MeetingType not found'}), 404

@meetingType_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    type = MeetingType.get_by_id(id)
    if type:
        db.session.delete(type)
        db.session.commit()
        return jsonify({'message': 'MeetingType deleted'}), 200
    else:
        return jsonify({'message': 'MeetingType not found'}), 404
