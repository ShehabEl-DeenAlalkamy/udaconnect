from app.config import _init_logger

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import logging

_init_logger()
_logger = logging.getLogger('udaconnect.connections_svc')

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    # TODO: check and test postgres connection
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
