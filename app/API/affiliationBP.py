from flask import Blueprint, jsonify, request
from app.models.affiliation import Affiliation
from app import db

affiliation_api_bp = Blueprint('affiliation_api', __name__, url_prefix='/api/v1/affiliations')

@affiliation_api_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    print(data)
    new_affiliation = Affiliation(
        affiliation_id=data['AffiliationID'],
        affiliation_name=data['AffiliationName'],
        label=data.get('Label'),
        parent_affiliation_id=data.get('ParentAffiliationID'),
        parent_affiliation_name=data.get('ParentAffiliationName')
    )
    db.session.add(new_affiliation)
    db.session.commit()
    return jsonify(new_affiliation.to_dict()), 201

def get_full_path(affiliation):
    """Returns the full hierarchical path of the affiliation."""
    if affiliation.parent_affiliation_id:
        parent = Affiliation.get_by_id(affiliation.parent_affiliation_id)
        return get_full_path(parent) + " > " + affiliation.affiliation_name
    else:
        return affiliation.affiliation_name

@affiliation_api_bp.route('/', methods=['GET'])
def index():
    """Returns a list of affiliations."""
    affiliations = Affiliation.query.all()

    # Check if a 'full_path' query parameter is present and set to 'true'
    include_full_path = request.args.get('full_path', '').lower() == 'true'
    
    affiliations_dicts = []
    for affiliation in affiliations:
        affiliation_dict = affiliation.to_dict()
        if include_full_path:
            affiliation_dict['full_path'] = get_full_path(affiliation)
        affiliations_dicts.append(affiliation_dict)
        
    return jsonify({'items': affiliations_dicts}), 200


@affiliation_api_bp.route('/<string:affiliation_id>', methods=['GET'])
def show(affiliation_id):
    affiliation = Affiliation.get_by_id(affiliation_id)
    if affiliation:
        return jsonify(affiliation.to_dict()), 200
    else:
        return jsonify({'message': 'Affiliation not found'}), 404

@affiliation_api_bp.route('/<string:affiliation_id>', methods=['PUT', 'PATCH'])
def update(affiliation_id):
    data = request.get_json()
    affiliation = Affiliation.get_by_id(affiliation_id)
    if affiliation:
        affiliation.update({
            'affiliation_id': data.get('AffiliationID'),
            'affiliation_name': data.get('AffiliationName'),
            'label': data.get('Label'),
            'parent_affiliation_id': data.get('ParentAffiliationID'),
            'parent_affiliation_name': data.get('ParentAffiliationName')
        })
        db.session.commit()
        return jsonify(affiliation.to_dict()), 200
    else:
        return jsonify({'message': 'Affiliation not found'}), 404

@affiliation_api_bp.route('/<string:affiliation_id>', methods=['DELETE'])
def delete(affiliation_id):
    affiliation = Affiliation.get_by_id(affiliation_id)
    if affiliation:
        db.session.delete(affiliation)
        db.session.commit()
        return jsonify({'message': 'Affiliation deleted'}), 200
    else:
        return jsonify({'message': 'Affiliation not found'}), 404
