from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from . import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app
