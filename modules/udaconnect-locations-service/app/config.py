import app.filters

from typing import List, Type
import os
import logging
import sys

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    KAFKA_BROKER = os.environ["KAFKA_BROKER"]
    KAFKA_TOPIC = os.environ["KAFKA_LOCATION_SVC_TOPIC"]


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    SECRET_KEY = os.getenv(
        "DEV_SECRET_KEY", "You can't see California without Marlon Widgeto's eyes"
    )
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "I'm Ron Burgundy?")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}


def _init_logger():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    handlers = [stderr_handler, stdout_handler]

    info_lvl_filter = app.filters.SingleLevelFilter(logging.INFO, False)
    info_lvl_filter_inverter = app.filters.SingleLevelFilter(
        logging.INFO, True)

    stdout_handler.addFilter(info_lvl_filter)
    stderr_handler.addFilter(info_lvl_filter_inverter)

    logging.basicConfig(level=logging.DEBUG,
                        format="[%(levelname)s]:%(name)s:%(asctime)s, %(message)s",
                        datefmt='%d/%m/%y, %H:%M:%S',
                        handlers=handlers)

    # TODO: remove if not needed when deployed in k8s cluster
    # disable common loggers for clean logging in local development
    logging.getLogger('kafka.conn').disabled = True
    logging.getLogger('kafka.consumer.subscription_state').disabled = True
    logging.getLogger('kafka.producer.record_accumulator').disabled = True
    logging.getLogger('kafka.consumer.fetcher').disabled = True
    logging.getLogger('kafka.producer.sender').disabled = True
    logging.getLogger('kafka.producer.kafka').disabled = True
    logging.getLogger('kafka.metrics').disabled = True
    logging.getLogger('kafka.metrics.metrics').disabled = True
    logging.getLogger('kafka.protocol.parser').disabled = True
    logging.getLogger('kafka.client').disabled = True
    logging.getLogger('kafka.coordinator').disabled = True
    logging.getLogger('kafka.coordinator.consumer').disabled = True
    logging.getLogger('kafka.cluster').disabled = True
    logging.getLogger('shapely.geos').disabled = True
    logging.getLogger('shapely.speedups._speedups').disabled = True
