from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    CORS(app)  # Enable CORS for the Chrome extension

    # Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app