from flask import Blueprint, jsonify, request
from app.models.country import Country
from app import db

country_api_bp = Blueprint('country_api', __name__, url_prefix='/api/v1/countries')

@country_api_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    new_country = Country(
        zone_id=data['ZoneID'],
        country_name=data['CountryName'],
        alpha2_code=data['Alpha2Code'],
        alpha3_code=data['Alpha3Code'],
        phone_prefix=data['PhonePrefix']
    )

    db.session.add(new_country)
    db.session.commit()
    return jsonify(new_country.to_dict()), 201

@country_api_bp.route('/', methods=['GET'])
def index():
    countries = Country.query.all()
    return jsonify({'items': [country.to_dict() for country in countries]}), 200

@country_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    country = Country.get_by_id(id)
    if country:
        return jsonify(country.to_dict()), 200
    else:
        return jsonify({'message': 'Country not found'}), 404

@country_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    country = Country.get_by_id(id)
    if country:
        country.update({
            'zone_id': data.get('ZoneID'),
            'country_name': data.get('CountryName'),
            'alpha2_code': data.get('Alpha2Code'),
            'alpha3_code': data.get('Alpha3Code'),
            'phone_prefix': data.get('PhonePrefix')
        })

        db.session.commit()
        return jsonify(country.to_dict()), 200
    else:
        return jsonify({'message': 'Country not found'}), 404

@country_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    success = Country.delete(id)
    if success:
        return jsonify({'message': 'Country deleted'}), 200
    else:
        return jsonify({'message': 'Country not found'}), 404
