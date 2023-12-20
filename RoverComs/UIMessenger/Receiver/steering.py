# steering.py
from flask import Blueprint, jsonify

steering_bp = Blueprint('steering', __name__)

@steering_bp.route('/default')
def turn_default():
    return jsonify({"message": "Driver has selected the default turning mode."})

@steering_bp.route('/situ')
def turn_situ():
    return jsonify({"message": "Driver has selected the situated turning mode."})

@steering_bp.route('/arc')
def turn_arc():
    return jsonify({"message": "Driver has selected the arc turn."})
