from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from flask_migrate import Migrate
from extensions import db  # Import db from extensions.py
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.librarian_routes import librarian_bp

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations from Config
    app.secret_key = Config.SECRET_KEY  # Set the secret key for sessions
    db.init_app(app)  # Bind the db instance to the app

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(librarian_bp, url_prefix='/librarian')

    from models.models import User  # Import your User model

    @app.route('/login', methods=['GET'])
    def redirect_to_auth_login():
        return redirect(url_for('auth.login_page'))


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)