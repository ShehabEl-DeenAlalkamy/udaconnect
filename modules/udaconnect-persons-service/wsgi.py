from app.udaconnect.grpc.server import Server
from app import create_app

import os


app = create_app(os.getenv("FLASK_ENV") or "test")

grpc_server = Server(app, port=5010)
grpc_server.serve()

if __name__ == "__main__":
    app.run(debug=True)
