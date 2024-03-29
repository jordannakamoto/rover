# ------------------------------------------------------------------------------- #
# app.py
# Main Driver Raspi Command Driver

# > Receives WebSocket messages from Client (Pilot's Laptop)
# > Parses and sends Speed updates to rover motors connected over I2C

# ------------------------------------------------------------------------------- #

import time
from flask import Flask                     # Flask Python WebServer
from flask_socketio import SocketIO, emit   # WebServer Connection Socket
from smbus2 import SMBus                    # I2C Bus Messaging Interface
import RPi.GPIO as GPIO                     # GPIO Pin Connection Interface
from Motors.TicI2C import TicI2C            # TicI2C Motor Controller Interface
import subprocess                           # Linux SubProcess


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
    
    # Home belt stepper to start position
    beltStep.homeRev()

    # Home bucket to start position
    #dumpBucket.homeRev()

    # --------------------------------

    ## WEB SERVER LISTENER: Listen for socket Messages
    socketio.run(app, host='0.0.0.0', port=4000)
 
    # ... Continue listening for socket Messages
    # no way of exiting safely yet
    # need to create some exit code...
    ###
# ================================================================= #


