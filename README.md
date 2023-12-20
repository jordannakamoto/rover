RoverComs is the Flask App
virtual environment
(like node modules, stores installed python libraries so they aren't installed globally on your computer)
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
```
pip install Flask
```
```
export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
export FLASK_ENV=development  # Enable development environment with debug mode
flask run
```

UserInterface is the React App
```
npm install
```
```
npm start
```

The Flask app is ran on port 4000
The UI app is ran on port 3000

they communicate with each other over a websocket connection.
then the flask app communicates with the raspberry pi over an additional websocket connection