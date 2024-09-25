from flask import Flask
import os
from flask_cors import CORS
from Microservice_Interface_Adapters.controllers.user_loginController import bp
def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'PBKDF2WithHmacSHA256')
    CORS(app)
    with app.app_context():
        app.register_blueprint(bp)
    return app
