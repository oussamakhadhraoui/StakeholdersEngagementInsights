from flask import Blueprint, render_template, request, redirect
import requests

invitation_view_bp = Blueprint('invitation_view', __name__, url_prefix='/invitations')

@invitation_view_bp.route('/new', methods=['GET'])
def new():
    return render_template('invitationsList.html')

@invitation_view_bp.route('/', methods=['POST'])
def create():
    data = request.form.to_dict()
    response = requests.post('http://localhost:5000/api/v1/invitations', json=data)
    return redirect('/invitations')

@invitation_view_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  

    api_url = f'http://localhost:5000/api/v1/invitations'
    response = requests.get(api_url)
    invitations_data = response.json()

    total_items = len(invitations_data['items'])
    total_pages = (total_items + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, total_items)
    invitations = invitations_data['items'][start_index:end_index]

    return render_template('invitationsList.html', invitations=invitations, pagination={
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_num': page - 1,
        'next_num': page + 1,
        'current_page': page,
        'total_pages': total_pages,
    })

@invitation_view_bp.route('/<int:id>', methods=['GET'])
def show(id):
    invitation = requests.get(f'http://localhost:5000/api/v1/invitations/{id}').json()

@invitation_view_bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    invitation = requests.get(f'http://localhost:5000/api/v1/invitations/{id}').json()
    return render_template('invitationsList.html', invitation=invitation)

@invitation_view_bp.route('/<int:id>', methods=['POST'])
def update(id):
    data = request.form.to_dict()
    requests.put(f'http://localhost:5000/api/v1/invitations/{id}', json=data)
    return redirect('/invitations')

@invitation_view_bp.route('/<int:id>', methods=['POST'])
def delete(id):
    requests.delete(f'http://localhost:5000/api/v1/invitations/{id}')
    return redirect('/invitations')
