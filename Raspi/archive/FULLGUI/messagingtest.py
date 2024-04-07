# ------------------------------------------------------------------------------- #
# messagingtest.py
# to test the messaging protocol between React/Raspi only
# without any class or method instantiation
# ------------------------------------------------------------------------------- #
# > Receives WebSocket messages from React
# > Handles HTTP Requests
# > Returns Reciept or HTTP 200 responses
# ------------------------------------------------------------------------------- #

from   flask           import Flask             # Flask Python WebServer
from   flask_socketio  import SocketIO, emit    # WebServer Connection Socket

## SETUP SERVER / WEB SOCKET OBJECTS
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

### CLIENT MESSAGE HANDLING
@socketio.on('message')
def handle_message(msg):

    if 'type' in msg and 'data' in msg:
        msgtype = msg['type']
        msgdata = msg['data']

    # Message Type Evaluations:
    if  msgtype == 'beltStepUp':
        pass

    elif msgtype == 'beltStepDown':
        pass

    elif msgtype == 'dumpBucketUp':
        pass

    elif msgtype == 'dumpBucketDown':
        pass

    elif msgtype == 'toggleConveyor':
        pass

    print( f'Received message: {msgtype} {msgdata}')
    # Emit response back to client
    emit('response', {'data': f'Received message: {msgtype} {msgdata}'})

###

# ================================================================= #
# HTTP API
#
# ================================================================= #
# /video_feed      :
# /update_settings : TODO change to video feed subURL
# /get_bitrate     : TODO change to video feed subURL

# Main Video Stream Access Point
@app.route('/video_feed')
def video_feed():
   print( '/video_feed route GET')
   return '/video_feed route GET', 200

# POST Route to update stream quality settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    print( '/update_settings route POST')
    return '/update_settings route POST', 200

# GET Route to provide bitrate information
@app.route('/get_bitrate', methods=['GET'])
def get_bitrate():
    print( '/get_bitrate route GET')
    return '/get_bitrate route GET', 200

# ================================================================= #
# MAIN DRIVER
# Execute main if program is run from command line `python messagingtest.py`
# ================================================================= #
if __name__ == "__main__":

    ## WEB SERVER LISTENER: Listen for socket Messages/HTTP Requests
    socketio.run(app, host='0.0.0.0',    port=4000)                 # WebSocket Messages
    # app.run(host='0.0.0.0', debug=False, port=4000, threaded=True)  # HTTP Requests

    ###
# ================================================================= #
