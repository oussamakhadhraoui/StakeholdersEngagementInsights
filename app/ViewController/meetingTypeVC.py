from flask import Blueprint, render_template, request, redirect
import requests

meetingType_view_bp = Blueprint('meetingType_view', __name__, url_prefix='/meeting-types')

@meetingType_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('newMeetingType.html')

@meetingType_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/meeting-types', json=data)
    return redirect('/meeting-types')

@meetingType_view_bp.route('/', methods=['GET'])
def index():
    types = requests.get('http://localhost:5000/api/v1/meeting-types').json()
    return render_template('meetingTypeList.html', types=types)

@meetingType_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    type = requests.get(f'http://localhost:5000/api/v1/meeting-types/{id}').json()
    return render_template('meetingType.html', type=type)

@meetingType_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    type = requests.get(f'http://localhost:5000/api/v1/meeting-types/{id}').json()
    return render_template('editMeetingType.html', type=type)

@meetingType_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/meeting-types/{id}', json=data)
    return redirect('/meeting-types')

@meetingType_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/meeting-types/{id}')
    return redirect('/meeting-types')
