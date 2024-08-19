from flask import Flask
from flask_socketio import SocketIO
from app.routes import main as routes_blueprint, socketio

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

    # Initialize SocketIO
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(routes_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    # Run the app on port 8080 instead of the default port 5000
    socketio.run(app, debug=True, port=8080)
    