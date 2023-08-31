from flask import Blueprint, render_template, request, redirect, current_app
import requests

affiliation_view_bp = Blueprint('affiliation_view', __name__, url_prefix='/affiliations')

@affiliation_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('affiliationList.html')

@affiliation_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations'
    response = requests.post(api_url, json=data)
    return redirect('/affiliations')

@affiliation_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations'
    response = requests.get(api_url)
    affiliations_data = response.json()

    total_items = len(affiliations_data['items'])
    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    affiliations = affiliations_data['items'][start_index:end_index]

    return render_template('affiliationList.html', affiliations=affiliations, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
    })

@affiliation_view_bp.route('/<string:affiliation_id>', methods=['GET'])
def show(affiliation_id):
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations/{affiliation_id}'
    affiliation = requests.get(api_url).json()


@affiliation_view_bp.route('/<string:affiliation_id>/edit', methods=['GET'])
def edit(affiliation_id):
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations/{affiliation_id}'
    affiliation = requests.get(api_url).json()
    return render_template('affiliationList.html', affiliation=affiliation)

@affiliation_view_bp.route('/<string:affiliation_id>', methods=['POST'])
def update(affiliation_id):
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations/{affiliation_id}'
    response = requests.put(api_url, json=data)
    return redirect('/affiliations')

@affiliation_view_bp.route('/<string:affiliation_id>', methods=['POST'])
def delete(affiliation_id):
    api_url = f'{current_app.config["API_BASE_URL"]}/affiliations/{affiliation_id}'
    response = requests.delete(api_url)
    return redirect('/affiliations')
