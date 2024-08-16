from flask import Flask
from .routes import main  # 'routes'에서 'main' 블루프린트 가져오기

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}
    
    # 블루프린트를 등록합니다.
    app.register_blueprint(main)

    return app
