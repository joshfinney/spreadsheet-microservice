from flask import Flask
from .models import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db(app)

    from .views import bp as cells_bp
    app.register_blueprint(cells_bp)

    return app