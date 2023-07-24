from flask import Blueprint, jsonify, request
from app.models.person import Person
from app import db
from flask_cors import cross_origin

person_api_bp = Blueprint('person_api', __name__, url_prefix='/api/v1/persons')

@person_api_bp.route('/', methods=['POST'])
@cross_origin()
def create():
    data = request.get_json()
    new_person = Person(
        first_name=data['FirstName'],
        last_name=data['LastName'],
        email=data['Email'],
        phone=data['Phone'],
        address=data['Address'],
        manager_id=data['ManagerID']
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person created'}), 201

@person_api_bp.route('/', methods=['GET'])
def index():
    people = Person.query.all()
    return jsonify([person.to_dict() for person in people]), 200

@person_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    person = Person.get_by_id(id)
    if person:
        return jsonify(person.to_dict()), 200
    else:
        return jsonify({'message': 'Person not found'}), 404

@person_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    person = Person.get_by_id(id)
    if person:
        person.update({
            'id': data.get('PersonID'),
            'first_name': data.get('FirstName'),
            'last_name': data.get('LastName'),
            'email': data.get('Email'),
            'phone': data.get('Phone'),
            'address': data.get('Address'),
            'manager_id': data.get('ManagerID'),
        })
        db.session.commit()
        return jsonify({'message': 'Person updated'}), 200
    else:
        return jsonify({'message': 'Person not found'}), 404

@person_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    person = Person.get_by_id(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted'}), 200
    else:
        return jsonify({'message': 'Person not found'}), 404
