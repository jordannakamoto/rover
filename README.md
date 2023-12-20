**RoverComs is the Flask App**
1. enter the directory used for the python api (flask)
```
cd RoverComs
```
2. setup virtual environment
(like node modules, stores installed python libraries so they aren't installed globally on your computer)
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. install flask
```
pip install Flask
```
4. launch the flask app. you can just use "python3 app.py" for testing also
```
export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
export FLASK_ENV=development  # Enable development environment with debug mode
flask run
```

**UserInterface is the React App**
1. enter the directory used for the react app
2. install node modules
```
cd UserInterface
npm install
```
3. test the react-app
```
npm start
```

The Flask app is ran on port 4000
The UI app is ran on port 3000

Todo:
Establish communication from port4000<->port3000 over websocket connection.
determine messages to be sent from operator to raspberry pi over an additional websocket connection
