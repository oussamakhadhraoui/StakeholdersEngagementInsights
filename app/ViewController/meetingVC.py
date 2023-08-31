from flask import Blueprint, render_template, request, redirect, current_app, flash
from app.models.meetingtype import MeetingType
import requests
import os
from werkzeug.utils import secure_filename
import tempfile
from app.Meeting_csv import transform_meeting, meeting_to_db

meeting_view_bp = Blueprint('meeting_view', __name__, url_prefix='/meetings')

@meeting_view_bp.route('/new', methods=['GET'])
def new():
    meeting_types = MeetingType.query.all()
    return render_template('upcomingMeetings.html', meeting_types=meeting_types)

@meeting_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/meetings'
    response = requests.post(api_url, json=data)
    return redirect('/meetings')

@meeting_view_bp.route('/csv_upload', methods=['POST'])
def csv_process():
    # Assuming you are receiving the CSV file as multipart/form-data
    file = request.files['csv_file']


    # Validate file type (Optional but recommended)
    if not file.filename.lower().endswith('.csv'):
        flash('Please upload a valid CSV file.', 'danger')
        return redirect('/meetings')


    # Create a temporary file to save the uploaded CSV data
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Call the transform_data method to process the CSV file
    transform_meeting(temp_file.name)

    # Clean up: Close and delete the temporary CSV file
    temp_file.close()
    os.remove(temp_file.name)

    # Call the csv_to_db method to read CSV data and add meetings to the database
    meeting_to_db()
    return redirect('/meetings')

@meeting_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  

    api_url = f'{current_app.config["API_BASE_URL"]}/meetings'
    response = requests.get(api_url)



    meetings_data = response.json()

    meeting_types = MeetingType.query.all()


    total_items = len(meetings_data['items'])
    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    meetings = meetings_data['items'][start_index:end_index]

    return render_template('upcomingMeetings.html', meetings=meetings, meeting_types=meeting_types, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
    })


@meeting_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meetings/{id}'
    meeting = requests.get(api_url).json()


@meeting_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meetings/{id}'
    meeting = requests.get(api_url).json()
    meeting_types_url = f'{current_app.config["API_BASE_URL"]}/meeting_types/'
    meeting_types = requests.get(meeting_types_url).json()
    return render_template('upcomingMeetings.html', meeting=meeting, meeting_types=meeting_types)


@meeting_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/meetings/{id}'
    response = requests.put(api_url, json=data)
    return redirect('/meetings')

@meeting_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/meetings/{id}'
    response = requests.delete(api_url)
    return redirect('/meetings')
