from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Jinja2에 enumerate를 필터로 추가
    app.jinja_env.globals.update(enumerate=enumerate)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
