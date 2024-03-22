# Drive 1
# Basic Driving Controls
# - Jordan and Gilberto
 
from smbus2 import SMBus, i2c_msg
import time
from flask import Flask
from flask_socketio import SocketIO, emit
from smbus2 import SMBus

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# |  class
# |  SmcG2I2
# |  usage: Object to control a single Pololu G2I2C motor
class SmcG2I2C(object): # TODO: give name to motor class
 
  speed = 0
  direction = 1
 
  def __init__(self, bus, address):
    self.bus = bus
    self.address = address
 
  # Sends the Exit Safe Start command, which is required to drive the motor.
  def exit_safe_start(self):
    write = i2c_msg.write(self.address, [0x83])
    self.bus.i2c_rdwr(write)
 
  # Sets the SMC's target speed (-3200 to 3200).
  def set_target_speed(self, speed):
    cmd = 0x85  # Motor forward
    if speed < 0:
      cmd = 0x86  # Motor reverse
      speed = -speed
    buffer = [cmd, speed & 0x1F, speed >> 5 & 0x7F]
    write = i2c_msg.write(self.address, buffer)
    self.bus.i2c_rdwr(write)
 
  # Gets the specified variable as an unsigned value.
  def get_variable(self, id):
    write = i2c_msg.write(self.address, [0xA1, id])
    read = i2c_msg.read(self.address, 2)
    self.bus.i2c_rdwr(write, read)
    b = list(read)
    return b[0] + 256 * b[1]
 
  # Gets the specified variable as a signed value.
  def get_variable_signed(self, id):
    value = self.get_variable(id)
    if value >= 0x8000:
      value -= 0x10000
    return value
 
  # Gets the target speed (-3200 to 3200).
  def get_target_speed(self):
    return self.get_variable_signed(20)
 
  # Gets a number where each bit represents a different error, and the
  # bit is 1 if the error is currently active.
  # See the user's guide for definitions of the different error bits.
  def get_error_status(self):
    return self.get_variable(0)

# DECLARATIONS
### MOTOR CONTROL BOARD DECLARATIONS
busNum = 11
# Name, PIN Bus , PIN Address, DebugMode?
MotorR  = SmcG2I2C(SMBus(busNum), 15)  # RightFront @ 16
MotorRB = SmcG2I2C(SMBus(busNum), 16)  # RightBack  @ 18
MotorL  = SmcG2I2C(SMBus(busNum), 17)  # LeftFront  @ 15
MotorLB = SmcG2I2C(SMBus(busNum), 18)  # LeftBack   @ ??
# Motor Left Back doesn't exist
# ------------


## SEND Speed Updates to all connected motors
# Set Target Speed from Client Message
# def speed_change
# ---------------------------------------------------------------------- 
def speed_change(left, right):
        # left, right speeds sent separately
        # Send speed to motor pairs
        MotorL.set_target_speed(-left)
        MotorLB.set_target_speed(-left)
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

#Socket IO
@socketio.on('message')
def handle_message(msg):
    # print('Received message:', msg)
    # Emit response back to client
    emit('response', {'data': 'Message received'})
    parts = msg.split()
 
    speed_change(int(parts[0]),int(parts[1]))
    # Emit succesfull speed change to client??
    # TODO: Error handling...
###

# Main Procedure
def main(): 
 
    # INTIALIZATION
 
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
    # --- END INITIALIZATION---  
 
 
    # Control Loop
    ### START: Listen for socket Messages
    socketio.run(app, host='0.0.0.0', port=4000)

    # need to create some exit code...
 
# Python Convention!
# If this is the main program root, run main loop
# Otherwise, if it's being imported as a module, just expose its methods
if __name__ == "__main__":
    main()
 
 
 