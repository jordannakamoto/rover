# ------------------------------------------------------------------------------- #
# app.py
# Main Driver Raspi Command Driver

# > Receives WebSocket messages from Client (Pilot's Laptop)
# > Parses and sends Speed updates to rover motors connected over I2C

# ------------------------------------------------------------------------------- #

import time
from   flask import Flask                       # Flask Python WebServer
from   flask_socketio import SocketIO, emit     # WebServer Connection Socket
from   smbus2 import SMBus                      # I2C Bus Messaging Interface
import RPi.GPIO as GPIO                         # GPIO Pin Connection Interface
from   Motors.TicI2C import TicI2C              # TicI2C Motor Controller Interface
import subprocess                               # Linux SubProcess

from   Video.VideoStreamer import VideoStreamer # TicI2C Motor Controller Interface


## SETUP SERVER / WEB SOCKET OBJECTS
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

## SETUP GPIO
GPIO.setmode(GPIO.BCM)                      # I don't know if this code is needed or if it is required by the motor classes themselves...
bus = SMBus(1)                              # Open a handle to "/dev/i2c-3", representing the I2C bus line. # ? Isn't this on bus 1

## SETUP MOTOR OBJECTS
beltStep = TicI2C(bus, 15, 45)              # Belt Frame Stepper Motor
#dumpBucket = TicI2C(bus,14, 0)             # Dump Bucket Motor

# Functions ============================================================ #
 
# ToggleConveyorOperation
# ---------------------------------------------------------------------- 
# runs conveyor code as its own Linux process
# to workaround problems with input()
def toggle_conveyor_operation():
  global conveyor_process

  if conveyor_process:
      print("Stopping conveyor... can take 4s")
      conveyor_process.terminate()  # Terminate the process
      conveyor_process.wait()  # Wait for process to terminate
      conveyor_process = None
  else:
      print("Starting conveyor...")
      conveyor_process = subprocess.Popen(['python3', 'conveyor2.py'])
# ======================================================================= # 
 
 
### CLIENT MESSAGE HANDLING
# For now, we only have one type of message which is (left,right speeds)
@socketio.on('message')
def handle_message(msg):

    # Message Type Evaluations:
    if   msg.type == 'beltStepUp':
        beltStep.move_cm(1)

    elif msg.type == 'beltStepDown':
        beltStep.move_cm(-1)

    elif msg.type == 'dumpBucketUp':
        #dumpBucket.move_cm(1)
        pass

    elif msg.type == 'dumpBucketDown':
        #dumpBucket.move_cm(-1)
        pass

    elif msg.type == 'toggleConveyor':
        toggle_conveyor_operation()

    print('Received message:', msg.type)
    # Emit response back to client
    emit('response', {'data': 'Message received'})

    # TODO: Error handling... Can't handle I2C motor status because the communication is one way
    # So we can't notify the client that the action executed successfully
###

# ================================================================= #
# MAIN DRIVER
# Execute main if program is run from command line `python app.py`
# ================================================================= #
if __name__ == "__main__":

    # STARTUP Procedure ------------- :
    
    # Disabled Code, Enable once Rover Components are Ready...
    # ENABLE AFTER MECHANICAL TODO: Hook Up Limit Switches to enable Homing /// #
    # Home belt stepper to start position
    # beltStep.homeRev()

    # Home bucket to start position
    #dumpBucket.homeRev()

    # ENABLE AFTER MECHANICAL TODO: Hook Up Video Camera ///////////////////// #
    # Instantiate VideoStreamer
    # streamer = VideoStreamer()
    # ///////////////////////////////////////////////////////////////////////// #

    # --------------------------------

    ## WEB SERVER LISTENER: Listen for socket Messages
    socketio.run(app, host='0.0.0.0',    port=4000)                 # WebSocket Messages
    app.run(host='0.0.0.0', debug=False, port=5000, threaded=True)  # HTTP Requests

 
    # ... Continue listening for socket Messages and HTTP Requests
    # no way of exiting safely yet
    # need to create some exit code...
    ###
# ================================================================= #


# ================================================================= #
# HTTP API
#
# ================================================================= #
# /video_feed      :
# /update_settings : TODO change to video feed subURL
# /get_bitrate     : TODO change to video feed subURL

# Main Stream Access Point
# - Access the video feed (streamed jpeg file) over 192.168.1.2/video_feed
@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(streamer.capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# POST Route to update stream quality settings
# - Gets params from client-side app and calls streamer.update_settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    data = request.json
    resolution = tuple(data.get('resolution'))
    jpeg_quality = int(data.get('jpeg_quality'))
    frame_rate = int(data.get('frame_rate'))
    if resolution and jpeg_quality is not None and frame_rate is not None:
        streamer.update_settings(resolution, jpeg_quality, frame_rate)
        return 'Settings updated successfully', 200
    else:
        return 'Invalid request data', 400

# GET Route to provide bitrate information
# Called periodically by the front end... runs a sub process for dumpcap/tshark
# - dumpcap: Captures wlan0 packets
# - tshark : Reads bitrate data from capture
# returns: average Bitrate information
@app.route('/get_bitrate', methods=['GET'])
def get_bitrate():
    capture_duration = 2  # seconds
    capture_file = "/tmp/capture.pcap"
    interface = "wlan0"  # or wlan0, or your relevant network interface
    
    # Start dumpcap to capture packets
    dumpcap_cmd = f"sudo dumpcap -a duration:{capture_duration} -w {capture_file} -i {interface}"
    subprocess.run(dumpcap_cmd.split())
    
    # Analyze the capture with tshark to compute the bitrate
    tshark_cmd = f"tshark -r {capture_file} -q -z io,stat,1"
    tshark_output = subprocess.run(tshark_cmd.split(), capture_output=True)
    
    # Extract the average bitrate
    try:
        output = tshark_output.stdout.decode('utf-8')
        lines = output.split('\n')
        bitrate_line = next(line for line in lines if "Duration" in line)
        bitrate_info = bitrate_line.split()
        avg_bitrate = bitrate_info[-2]  # Assuming the second last entry is the average bitrate
    except Exception as e:
        return jsonify({"error": "Failed to compute bitrate", "details": str(e)}), 500

    # Remove the capture file to save space
    os.remove(capture_file)

    # Send the bitrate information back to the client
    return jsonify({"avg_bitrate": avg_bitrate}), 200