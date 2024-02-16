# app.py
from flask import Flask
from UIMessenger.Receiver._receiver import register_namespaces
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Register UIMessenger
register_namespaces(socketio)

@socketio.on('message')
def handle_message(msg):
    print('Received message:', msg)
    # Emit response back to client
    emit('response', {'data': 'Message received'})


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=4000)