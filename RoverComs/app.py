# app.py
from flask import Flask
from UIMessenger.Receiver._receiver import register_namespaces
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register UIMessenger
register_namespaces(socketio)

if __name__ == "__main__":
    socketio.run(app, port=4000)
