from flask import Blueprint, render_template, request, redirect
import requests
import json

role_view_bp = Blueprint('role_view', __name__, url_prefix='/roles')

@role_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('newRole.html')

@role_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/roles', json=data)
    return redirect('/roles')

@role_view_bp.route('/', methods=['GET'])
def index():
    roles = requests.get('http://localhost:5000/api/v1/roles').json()
    return render_template('rolesList.html', roles=roles)

@role_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    role = requests.get(f'http://localhost:5000/api/v1/roles/{id}').json()
    return render_template('role.html', role=role)

@role_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    role = requests.get(f'http://localhost:5000/api/v1/roles/{id}').json()
    return render_template('editRole.html', role=role)

@role_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/roles/{id}', json=data)
    return redirect('/roles')

@role_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/roles/{id}')
    return redirect('/roles')
