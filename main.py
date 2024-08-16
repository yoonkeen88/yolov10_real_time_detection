from flask import Flask
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}
    
    with app.app_context():
        from app.routes import main
        app.register_blueprint(main)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
