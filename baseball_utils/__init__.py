from config import Config

from flask import Flask
from flask_compress import Compress


compress = Compress()


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    compress.init_app(app)

    from baseball_utils.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
