from app.config import _init_logger

from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import logging

_init_logger()
_logger = logging.getLogger('udaconnect.connections_svc')

db = SQLAlchemy()


def create_app(env=None):
    from app.udaconnect.grpc.clients import PersonStub
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.before_request
    def before_request():
        if 'grpc_client' not in g:
            _logger.info("initializing grpc client..")
            g.grpc_client = PersonStub(host='localhost', port=5010)

    @app.teardown_appcontext
    def teardown_grpc_client(exception):
        grpc_client = g.pop('grpc_client', None)

        if grpc_client is not None:
            _logger.info("removing grpc client..")
            del grpc_client

    # TODO: check and test postgres connection
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
