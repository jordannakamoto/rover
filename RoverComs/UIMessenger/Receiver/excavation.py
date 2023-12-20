# excavation.py
from flask import Blueprint, jsonify

excavation_bp = Blueprint('excavation', __name__)

@excavation_bp.route('/lift')
def excavation_lift():
    return jsonify({"message": "The Driver has selected the action for lifting the load."})

@excavation_bp.route('/drop')
def excavation_drop():
    return jsonify({"message": "The Driver has selected the action for dropping the load."})

@excavation_bp.route('/deliver')
def excavation_deliver():
    return jsonify({"message": "The Driver has selected the action for delivering the load."})