from app.config import _init_logger

from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
import logging

_init_logger()
_logger = logging.getLogger('udaconnect.locations_svc')

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.udaconnect.message_producer import MessageProducer
    from app.udaconnect.message_consumer import MessageConsumer

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect Location API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    kafka_consumer = MessageConsumer(
        app.config['KAFKA_BROKER'], app.config['KAFKA_TOPIC'], app)
    kafka_consumer.start()

    @app.before_request
    def before_request():
        if 'kafka_producer' not in g:
            g.kafka_producer = MessageProducer(
                app.config['KAFKA_BROKER'], app.config['KAFKA_TOPIC'])

    @app.teardown_appcontext
    def teardown_kafka_producer(exception):
        kafka_producer = g.pop('kafka_producer', None)

        if kafka_producer is not None:
            del kafka_producer

    # TODO: check and test both kafka and postgres connections
    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
