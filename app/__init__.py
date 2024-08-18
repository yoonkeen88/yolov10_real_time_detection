from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}
    
    app.register_blueprint(main)

    return app
