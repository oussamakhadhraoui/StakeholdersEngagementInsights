from flask import Blueprint, jsonify, request
from app.models.zone import Zone
from app import db

zone_api_bp = Blueprint('zone_api', __name__, url_prefix='/api/v1/zones')

@zone_api_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    new_zone = Zone(
        zone_name=data['ZoneName'],
        timezone=data['Timezone']
    )

    db.session.add(new_zone)
    db.session.commit()
    return jsonify(new_zone.to_dict()), 201

@zone_api_bp.route('/', methods=['GET'])
def index():
    zones = Zone.query.all()
    return jsonify({'items': [zone.to_dict() for zone in zones]}), 200

@zone_api_bp.route('/<int:id>', methods=['GET'])
def show(id):
    zone = Zone.get_by_id(id)
    if zone:
        return jsonify(zone.to_dict()), 200
    else:
        return jsonify({'message': 'Zone not found'}), 404

@zone_api_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id):
    data = request.get_json()
    zone = Zone.get_by_id(id)
    if zone:
        zone.update({
            'zone_name': data.get('ZoneName'),
            'timezone': data.get('Timezone')
        })
        
        db.session.commit()
        return jsonify(zone.to_dict()), 200
    else:
        return jsonify({'message': 'Zone not found'}), 404

@zone_api_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    success = Zone.delete(id)
    if success:
        return jsonify({'message': 'Zone deleted'}), 200
    else:
        return jsonify({'message': 'Zone not found'}), 404
