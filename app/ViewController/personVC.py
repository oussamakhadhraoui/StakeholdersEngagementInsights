from flask import Blueprint, render_template, request, redirect, current_app, flash
import requests
import os
import tempfile
from app.Persons_csv import transform_persons, person_to_db

person_view_bp = Blueprint('person_view', __name__, url_prefix='/persons')

@person_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('peopleList.html')

@person_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/persons'
    response = requests.post(api_url, json=data)
    return redirect('/persons')

@person_view_bp.route('/csv_upload', methods=['POST'])
def csv_upload():

    file = request.files['csv_file']


    if not file.filename.lower().endswith('.csv'):
      flash('Please upload a valid CSV file.', 'danger')
      return redirect('/persons')



    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)


    transform_persons(temp_file.name)

  
    temp_file.close()
    os.remove(temp_file.name)


    person_to_db()

    return redirect('/persons')


@person_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    api_url = f'{current_app.config["API_BASE_URL"]}/persons'
    response = requests.get(api_url)
    persons_data = response.json()
    
    total_items = len(persons_data['items'])

    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    persons = persons_data['items'][start_index:end_index]

    return render_template('peopleList.html', persons=persons, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
        'total_items': total_items,  # Add total_items to the pagination data
    })


@person_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/persons/{id}'
    person = requests.get(api_url).json()

@person_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/persons/{id}'
    person = requests.get(api_url).json()
    return render_template('peopleList.html', person=person)

@person_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    api_url = f'{current_app.config["API_BASE_URL"]}/persons/{id}'
    response = requests.put(api_url, json=data)
    return redirect('/persons')

@person_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    api_url = f'{current_app.config["API_BASE_URL"]}/persons/{id}'
    response = requests.delete(api_url)
    return redirect('/persons')