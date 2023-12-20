# receiver.py
from .steering import steering_bp
from .excavation import excavation_bp

def register_blueprints(app):
    """
    Define Messaging Endpoints
    """
    app.register_blueprint(steering_bp, url_prefix='/steering/turning')
    app.register_blueprint(excavation_bp, url_prefix='/excavation')
