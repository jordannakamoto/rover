# Most basic setup for Flask receiver server
# app.py
from flask import Flask
from UIMessenger.Receiver._receiver import register_namespaces
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# -----------------------------------------------#
# REPLACE ALL OF THIS WITH CODE OFF OF THE RASPI #
# -----------------------------------------------#

# Register UIMessenger
register_namespaces(socketio)

# Listen for socket messages
@socketio.on('message')
def handle_message(msg):
    print('Received message:', msg)
    # Emit response back to client
    emit('response', {'data': 'Message received'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=4000) # Run app on network