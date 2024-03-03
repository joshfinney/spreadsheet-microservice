from flask import Flask
from .models import init_db
from .views import bp as cells_bp

def create_app(config_class):
    app = Flask(__name__)

    app.config.from_object(config_class)

    if config_class == "app.config.Config":
        init_db(app)
    elif config_class == "app.config.FirebaseConfig":
        pass

    app.register_blueprint(cells_bp)

    return app