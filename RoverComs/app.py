# app.py
from flask import Flask
from UIMessenger.Receiver._receiver import register_blueprints

app = Flask(__name__)

# Register blueprints
register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True, port=4000)
