from flask import Blueprint, render_template, request, redirect
from app.models.meetingtype import MeetingType
import requests
import json

meeting_view_bp = Blueprint('meeting_view', __name__, url_prefix='/meetings')

@meeting_view_bp.route('/new', methods=['GET'])
def new():
    meeting_types = MeetingType.query.all()
    return render_template('newMeeting.html', meeting_types=meeting_types)

@meeting_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/meetings', json=data)
    return redirect('/meetings')

@meeting_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    meetings = requests.get(f'http://localhost:5000/api/v1/meetings?page={page}').json()
    return render_template('home.html', meetings=meetings['items'], pagination=meetings)


@meeting_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    meeting = requests.get(f'http://localhost:5000/api/v1/meetings/{id}').json()
    return render_template('meeting.html', meeting=meeting)

@meeting_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    meeting = requests.get(f'http://localhost:5000/api/v1/meetings/{id}').json()
    return render_template('editMeeting.html', meeting=meeting)

@meeting_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/meetings/{id}', json=data)
    return redirect('/meetings')

@meeting_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/meetings/{id}')
    return redirect('/meetings')
