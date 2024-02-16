#excavation.py
from flask_socketio import Namespace, emit

class ExcavationNamespace(Namespace):
    def on_lift(self, data):
        emit('response', {"message": "The Driver has selected the action for lifting the load."})

    def on_drop(self, data):
        emit('response', {"message": "The Driver has selected the action for dropping the load."})

    def on_deliver(self, data):
        emit('response', {"message": "The Driver has selected the action for delivering the load."})
