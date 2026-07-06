# app/__init__.py
# This file turns the "app" folder into a Python package AND
# contains the "application factory" — a function that builds and configures our Flask app.

from flask import Flask

def create_app():
    # Create the Flask application instance.
    # __name__ tells Flask "look for templates/static relative to this file's location"
    app = Flask(__name__)

    # Import routes here (inside the function) to avoid circular import errors.
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app