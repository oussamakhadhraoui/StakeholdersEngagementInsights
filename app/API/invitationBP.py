from flask import Blueprint, jsonify, request
from app.models.invitation import Invitation
from app.models.meeting import Meeting
from app.models.person import Person
from app.models.role import Role
from app import db
from flask_cors import cross_origin

invitation_api_bp = Blueprint('invitation_api', __name__, url_prefix='/api/v1/invitations')

@invitation_api_bp.route('/', methods=['POST'])
@cross_origin()
def create():
    data = request.get_json()
    errors = []
    
    meeting = Meeting.get_by_id(data['MeetingID'])
    if not meeting:
        errors.append("Meeting not found")
    
    person = Person.get_by_id(data['PersonID'])
    if not person:
        errors.append("Person not found")
    
    role = Role.get_by_id(data['RoleID'])
    if not role:
        errors.append("Role not found")

    if errors:
     return jsonify({'message': errors}), 404
    
    new_invitation = Invitation(
        meeting_id=data['MeetingID'],
        person_id=data['PersonID'],
        role_id=data['RoleID'],
        status=data['Status']
    )
    db.session.add(new_invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation created'}), 201

@invitation_api_bp.route('/', methods=['GET'])
def index():
    invitations = Invitation.query.all()
    return jsonify({'items': [invitation.to_dict() for invitation in invitations]}), 200

@invitation_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    invitation = Invitation.get_by_id(id)
    if invitation:
        return jsonify(invitation.to_dict()), 200
    else:
        return jsonify({'message': 'Invitation not found'}), 404

@invitation_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    invitation = Invitation.get_by_id(id)
    if invitation:
        invitation.update({
            'meeting_id': data.get('MeetingID'),
            'person_id': data.get('PersonID'),
            'role_id': data.get('RoleID'),
            'status': data.get('Status'),
        })
        db.session.commit()
        return jsonify({'message': 'Invitation updated'}), 200
    else:
        return jsonify({'message': 'Invitation not found'}), 404

@invitation_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    invitation = Invitation.get_by_id(id)
    if invitation:
        db.session.delete(invitation)
        db.session.commit()
        return jsonify({'message': 'Invitation deleted'}), 200
    else:
        return jsonify({'message': 'Invitation not found'}), 404