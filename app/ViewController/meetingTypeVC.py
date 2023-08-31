from flask import Blueprint, render_template, request, redirect, current_app
import requests

meetingType_view_bp = Blueprint('meetingType_view', __name__, url_prefix='/meeting-types')

@meetingType_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('meetingTypesList.html')

@meetingType_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types'
    response = requests.post(api_url, json=data)
    return redirect('/meeting-types')

@meetingType_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types'
    response = requests.get(api_url)
    types_data = response.json()

    total_items = len(types_data['items'])
    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    types = types_data['items'][start_index:end_index]

    return render_template('meetingTypesList.html', types=types, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
    })

@meetingType_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types/{id}'
    type = requests.get(api_url).json()


@meetingType_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types/{id}'
    type = requests.get(api_url).json()
    return render_template('meetingTypesList.html', type=type)

@meetingType_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types/{id}'
    response = requests.put(api_url, json=data)
    return redirect('/meeting-types')

@meetingType_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meeting-types/{id}'
    response = requests.delete(api_url)
    return redirect('/meeting-types')