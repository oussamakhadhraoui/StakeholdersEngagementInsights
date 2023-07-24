from flask import Blueprint, jsonify, request
from app.models.role import Role
from app import db
from flask_cors import cross_origin

role_api_bp = Blueprint('role_api', __name__, url_prefix='/api/v1/roles')

@role_api_bp.route('/', methods=['POST'])
@cross_origin()
def create():
    data = request.get_json()
    new_role = Role(
        role_name=data['role_name']
    )
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'Role created'}), 201

@role_api_bp.route('/', methods=['GET'])
def index():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200

@role_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    role = Role.get_by_id(id)
    if role:
        return jsonify(role.to_dict()), 200
    else:
        return jsonify({'message': 'Role not found'}), 404

@role_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    role = Role.get_by_id(id)
    if role:
        role.update({
            'id': data.get('RoleID'),
            'role_name': data.get('RoleName'),
        })
        db.session.commit()
        return jsonify({'message': 'Role updated'}), 200
    else:
        return jsonify({'message': 'Role not found'}), 404

@role_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    role = Role.get_by_id(id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Role deleted'}), 200
    else:
        return jsonify({'message': 'Role not found'}), 404
