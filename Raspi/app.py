# ------------------------------------------------------------------------------- #
# app.py
# Main Driver Raspi Command Driver

# > Receives WebSocket messages from Client (Pilot's Laptop)
# > Parses and sends Speed updates to array of rover motors connected over I2C

# ------------------------------------------------------------------------------- #

import time
from flask import Flask
from flask_socketio import SocketIO, emit
from smbus2 import SMBus
from Motors.G2MotorController import G2MotorController

### SETUP SERVER / WEB SOCKET OBJECTS
# Doesn't have connection security checking
 
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


### MOTOR CONTROL BOARD DECLARATIONS
busNum = 11
# Name, PIN Bus , PIN Address, DebugMode?
MotorR  = G2MotorController("MotorR", SMBus(busNum), 15, False)  # RightFront @ 16
MotorRB = G2MotorController("MotorRB", SMBus(busNum), 16, False)  # RightBack  @ 18
MotorL  = G2MotorController("MotorL", SMBus(busNum), 17, False)  # LeftFront  @ 15
MotorLB = G2MotorController("MotorLB", SMBus(busNum), 18, False)  # LeftBack   @ ??
###
 
## SEND Speed Updates to all connected motors
# Set Target Speed from Client Message
# def speed_change
# ---------------------------------------------------------------------- 
def speed_change(left, right):
        # left, right speeds sent separately
        # Send speed to motor pairs
        MotorL.set_target_speed(-left)
        # MotorLB.set_target_speed(-left)
        MotorR.set_target_speed(right)
        MotorRB.set_target_speed(right)
        # ---------------------------

        # ERROR Reporting...
        # At end of every command issued, 
        error_status = MotorR.get_error_status()
        if error_status == 0x0000:
            pass
        else:
            print("MotorR Error status: 0x{:04X}".format(error_status))
            
        error_status = MotorRB.get_error_status()
        if error_status == 0x0000:
            print("Speed R:", right) # If no error, print speed
        else:
            print("MotorRB Error status: 0x{:04X}".format(error_status))
        error_status = MotorL.get_error_status()
        if error_status == 0x0000:
           pass
        else:
            print("MotorL Error status: 0x{:04X}".format(error_status))
        error_status = MotorLB.get_error_status()
        if error_status == 0x0000:
            print("Speed L:", left) # If no error, print speed
        else:
            print("MotorLB Error status: 0x{:04X}".format(error_status))
# ---------------------------------------------------------------------- 
 
 
### CLIENT MESSAGE HANDLING
# For now, we only have one type of message which is (left,right speeds)
@socketio.on('message')
def handle_message(msg):
    print('Received message:', msg)
    # Emit response back to client
    emit('response', {'data': 'Message received'})
    parts = msg.split()
 
    speed_change(int(parts[0]),int(parts[1]))
    # Emit succesfull speed change to client??
    # TODO: Error handling...
###
 
if __name__ == "__main__":
 
    ### INTIALIZATION:
 
    # motorR startup
    MotorR.exit_safe_start()
    error_status = MotorR.get_error_status()
    if error_status == 0x0000:
        print("Right Front Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
 
    # motorRB startup
    MotorRB.exit_safe_start()
    error_status = MotorRB.get_error_status()
    if error_status == 0x0000:
        print("Right Rear Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
 
    # motorL startup
    MotorL.exit_safe_start()
    error_status = MotorL.get_error_status()
    if error_status == 0x0000:
        print("Left Front Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))

    # motorLB startup
    MotorLB.exit_safe_start()
    error_status = MotorLB.get_error_status()
    if error_status == 0x0000:
        print("Left Rear Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
    # ### --- END INITIALIZATION--- 

    ### START: Listen for socket Messages
    socketio.run(app, host='0.0.0.0', port=4000)
 
    # ... Continue listening for socket Messages
    # no way of exiting safely yet
    # need to create some exit code...
    ###