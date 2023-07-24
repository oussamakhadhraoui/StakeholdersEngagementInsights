from flask import Blueprint, render_template, request, redirect
import requests
import json

invitation_view_bp = Blueprint('invitation_view', __name__, url_prefix='/invitations')

@invitation_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('newInvitation.html')

@invitation_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/invitations', json=data)
    return redirect('/invitations')

@invitation_view_bp.route('/', methods=['GET'])
def index():
    invitations = requests.get('http://localhost:5000/api/v1/invitations').json()
    return render_template('invitationsList.html', invitations=invitations)

@invitation_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    invitation = requests.get(f'http://localhost:5000/api/v1/invitations/{id}').json()
    return render_template('invitation.html', invitation=invitation)

@invitation_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    invitation = requests.get(f'http://localhost:5000/api/v1/invitations/{id}').json()
    return render_template('editInvitation.html', invitation=invitation)

@invitation_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/invitations/{id}', json=data)
    return redirect('/invitations')

@invitation_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/invitations/{id}')
    return redirect('/invitations')
