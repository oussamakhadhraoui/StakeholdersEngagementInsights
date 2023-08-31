from flask import Blueprint, render_template, request, redirect, current_app, flash
import requests
import os
import tempfile
from app.Attendance_csv import transform_attendance, attendance_to_db

attendance_view_bp = Blueprint('attendance_view', __name__, url_prefix='/attendances')

@attendance_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('attendanceList.html')

@attendance_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances'
    response = requests.post(api_url, json=data)
    return redirect('/attendances')

@attendance_view_bp.route('/csv_upload', methods=['POST'])
def csv_upload():
    # Assuming you are receiving the CSV file as multipart/form-data
    file = request.files['csv_file']

    # Validate file type (Optional but recommended)
    if not file.filename.endswith('.csv'):
        flash('Please upload a valid CSV file.', 'danger')
        return redirect('/attendances')

    # Create a temporary file to save the uploaded CSV data
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)

    # Call the transform_data method to process the CSV file
    transform_attendance(temp_file.name)

    # Clean up: Close and delete the temporary CSV file
    temp_file.close()
    os.remove(temp_file.name)

    # Call the attendance_to_db method to read CSV data and add attendance to the database
    attendance_to_db()

    return redirect('/attendances')

@attendance_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances'
    response = requests.get(api_url)
    attendances_data = response.json()

    total_items = len(attendances_data['items'])
    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    attendances = attendances_data['items'][start_index:end_index]

    return render_template('attendanceList.html', attendances=attendances, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
    })

@attendance_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances/{id}'
    attendance = requests.get(api_url).json()


@attendance_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances/{id}'
    attendance = requests.get(api_url).json()
    return render_template('attendanceList.html', attendance=attendance)

@attendance_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances/{id}'
    response = requests.put(api_url, json=data)
    return redirect('/attendances')

@attendance_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/attendances/{id}'
    response = requests.delete(api_url)
    return redirect('/attendances')
