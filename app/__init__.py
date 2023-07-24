from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask import render_template

db = SQLAlchemy()
migrate = Migrate()

from app.models import init_db
from app.API.meetingBP import meeting_api_bp
from app.API.meetingTypeBP import meetingType_api_bp
from app.API.personBP import person_api_bp
from app.API.roleBP import role_api_bp
from app.API.invitationBP import invitation_api_bp

from app.ViewController.meetingVC import meeting_view_bp
from app.ViewController.meetingTypeVC import meetingType_view_bp
from app.ViewController.personVC import person_view_bp
from app.ViewController.roleVC import role_view_bp
from app.ViewController.invitationVC import invitation_view_bp

'''from flask_swagger_ui import get_swaggerui_blueprint'''

def create_app():
    '''TO USE SWAGGER LOCALLY
    app = Flask(__name__, static_folder='../static')
    SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = 'http://localhost:5000/api/v1/swagger.yaml'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)'''
    app = Flask(__name__)
    '''CORS for swagger
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])'''
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    '''app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)'''


    'API BP'
    app.register_blueprint(meeting_api_bp, url_prefix='/api/v1/meetings')
    app.register_blueprint(meetingType_api_bp, url_prefix='/api/v1/meeting-types')
    app.register_blueprint(person_api_bp, url_prefix='/api/v1/persons')
    app.register_blueprint(role_api_bp, url_prefix='/api//v1/roles')
    app.register_blueprint(invitation_api_bp, url_prefix='/api/v1/invitations')


    'View BP'
    app.register_blueprint(meeting_view_bp, url_prefix='/meetings')
    app.register_blueprint(meetingType_view_bp, url_prefix='/meeting-types')
    app.register_blueprint(person_view_bp, url_prefix='/persons')
    app.register_blueprint(role_view_bp, url_prefix='/roles')
    app.register_blueprint(invitation_view_bp, url_prefix='/invitations')


    @app.route('/')
    def home():
     return render_template('home.html')

    return app
