from flask import g, current_app
import json


def send_data(data, action):
    message = {
        "action": action,
        "data": data
    }
    current_app.logger.info(f"sending message to kafka: {message}")
    g.kafka_producer.send(
        current_app.config['KAFKA_TOPIC'], json.dumps(message).encode())
