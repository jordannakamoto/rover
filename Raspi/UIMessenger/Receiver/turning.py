# turning.py
from flask_socketio import Namespace, emit

class TurningNamespace(Namespace):
    def on_default(self, data):
        emit('response', {"message": "Driver has selected the default turning mode."})

    def on_situ(self, data):
        emit('response', {"message": "Driver has selected the situated turning mode."})

    def on_arc(self, data):
        emit('response', {"message": "Driver has selected the arc turn."})
