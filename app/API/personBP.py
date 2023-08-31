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
        affiliation_id=data['AffiliationID'],
        country_id=data['CountryID'],
        manager_id=data['ManagerID'] if 'ManagerID' in data and data['ManagerID'] is not None else None
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({'message': 'Person created'}), 201


@person_api_bp.route('/', methods=['GET'])
def index():
    people = Person.query.all()
    return jsonify({'items': [person.to_dict() for person in people]}), 200

def id_to_email_mapping(id):
    return Person.get_by_id(id).email

@person_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    email = id_to_email_mapping(id)
    person = Person.get_by_email(email)
    if person:
        return jsonify(person.to_dict()), 200
    else:
        return jsonify({'message': 'Person not found'}), 404

@person_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    email = id_to_email_mapping(id)
    person = Person.get_by_email(email)
    data = request.get_json()
    if person:
        update_data = {
            'first_name': data.get('FirstName'),
            'last_name': data.get('LastName'),
            'email': data.get('Email'),
            'phone': data.get('Phone'),
            'address': data.get('Address'),
            'affiliation_id': data.get('AffiliationID'),
            'country_id': data.get('CountryID')
        }
        if 'ManagerID' in data:
            update_data['manager_id'] = data['ManagerID'] if data['ManagerID'] is not None else None
        person.update(update_data)
        db.session.commit()
        return jsonify({'message': 'Person updated'}), 200
    else:
        return jsonify({'message': 'Person not found'}), 404

@person_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    email = id_to_email_mapping(id)
    person = Person.get_by_email(email)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted'}), 200
    else:
        return jsonify({'message': 'Person not found'}), 404
