import logging
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
jwt = JWTManager()

def mydb():
    app = Flask(__name__)
    scheduler = BackgroundScheduler()

    # Define UPLOAD_FOLDER before using it
    UPLOAD_FOLDER = '/home/ytp/Desktop/Project_angular/TechNotifier/src/assets/uploads'

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USERNAME')
    app.config['JWT_SECRET_KEY'] = 'qwertyuiop'

    # Now it's safe to set the UPLOAD_FOLDER in the config
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Configure CORS


    CORS(app, resources={
        r"/user/*": {"origins": "http://localhost:4200"},
        r"/subscriptions": {"origins": "http://localhost:4200"}
    })

    # Route to serve uploaded files, checking if they exist
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(file_path):
            return send_from_directory(UPLOAD_FOLDER, filename)
        else:
            return "File not found", 404

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Flask app initialized with configuration.")

    # Import TaskService and set up scheduler within the function to avoid circular import
    from tech.app.appMain.Services.task import fetch_updates

    # Wrapper function to ensure app context is used
    def run_fetch_and_create_updates():
        with app.app_context():
            fetch_updates()

    # Set up scheduler job (running every minute)
    scheduler.add_job(run_fetch_and_create_updates, 'interval', minutes=120, id='fetch_updates_task')
    scheduler.start()

    return app

# minutes=10