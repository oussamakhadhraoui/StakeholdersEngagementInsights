from flask import Blueprint, render_template, request, redirect
import requests
import json

person_view_bp = Blueprint('person_view', __name__, url_prefix='/persons')

@person_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('newPerson.html')

@person_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/persons', json=data)
    return redirect('/persons')

@person_view_bp.route('/', methods=['GET'])
def index():
    persons = requests.get('http://localhost:5000/api/v1/persons').json()
    return render_template('personsList.html', persons=persons)

@person_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    person = requests.get(f'http://localhost:5000/api/v1/persons/{id}').json()
    return render_template('person.html', person=person)

@person_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    person = requests.get(f'http://localhost:5000/api/v1/persons/{id}').json()
    return render_template('editPerson.html', person=person)

@person_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/persons/{id}', json=data)
    return redirect('/persons')

@person_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/persons/{id}')
    return redirect('/persons')
