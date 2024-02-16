# receiver.py
from .turning import TurningNamespace
from .excavation import ExcavationNamespace

def register_namespaces(socketio):
    """
    Define WebSocket Namespaces
    """
    socketio.on_namespace(TurningNamespace('/turning'))
    socketio.on_namespace(ExcavationNamespace('/excavation'))
