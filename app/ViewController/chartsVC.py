from flask import Blueprint, render_template

charts_view_bp = Blueprint('charts_view', __name__, url_prefix='/charts')

@charts_view_bp.route('/')
def display_chart():
    return render_template('charts.html')  # Always render the combined chart template
