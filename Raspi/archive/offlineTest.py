# OFFLINE TESTING
# Run/Control directly from Raspberry Pi terminal
 
# HOW TO RUN
# script is located on Desktop
# from root ~/ cd Desktop
# `sudo python3 jordan1.py`
# STOP script from Terminal with Ctrl+C
 
# HOW TO OPERATE:
# for testing a single motor rotating at various speeds, forward and backwards
# press 1-9 to set motor speed
# press ` tilde to the left of the numbers to swithc direction
# press 0 to halt the motor
 
 
# Solving Error 0x0001 Motor Error
# ?Acelleration/Decelleration implementation
# ?Rate Limiter
# Might need to incorporate some kind of rate limiter on speed control...?
 
# - Jordan and Gilberto
 
from smbus2 import SMBus, i2c_msg
import keyboard
import time
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
 
# |  class
# |  Keyboard Control Interface (motorR,motorL)
# |  Controls not One but Two motors and their logic!
# |
# |  usage: Instantiate in main loop to wrap a set of motors with control
# |  important: currently only handles one motor!
class KeyboardControlInterface(object): #two 
 
    def __init__(self, motorL, motorR, motorRB):
        self.motorL = motorL
        self.motorR = motorR
        self.motorRB = motorRB
 
    def handle_key_event(self, event):
        key = event.name
 
 
        # STEP 1: Since Right and Right back are always the same speed, only preform calculation once.
 
 
        # Keyboard Control -> Coordinate
        # 0 | Stop
        if key == '0': 
            self.motorR.speed = 0
            self.motorL.speed = 0
        # * | Both motors reverse
        elif key == 's':
            self.motorR.direction *= -1
            self.motorL.direction *= -1
        # 7 | Left Motor Accelerate
        elif key == '7':
            if(self.motorL.speed <= 2800):
                self.motorL.speed += 400  # Increment Left Motor by 400
        # 9 | Right Motor Accelerate
        elif key == '3':
            if(self.motorR.speed <= 2800):
                self.motorR.speed += 400  # Increment Right Motor by 400
        # 1 | Left Motor Deccelerate
        elif key == '1':
            if(self.motorL.speed >= -2800):
                self.motorL.speed -= 400  # Decrement Left Motor by 400
        # 3 | Right Motor Deccelerate
        elif key == '9':
            if(self.motorR.speed >= -2800):
                self.motorR.speed -= 400  # Decrement Right Motor by 400
        else:
            return
 
        # STEP 2:
        # Send calculation to motor pair
 
        # set new speeds on Right and Left Motor Groups
        new_speed = self.motorR.speed * self.motorR.direction
        self.motorR.set_target_speed(new_speed)
        self.motorRB.set_target_speed(new_speed)
 
        new_speed2 = self.motorL.speed * self.motorL.direction
        self.motorL.set_target_speed(new_speed2)
 
        # At end of every command issued, Error Reporting
        error_status = self.motorR.get_error_status()
        if error_status == 0x0000:
            print("Speed R:", self.motorR.speed) # If no error, print speed
        else:
            print("Error status: 0x{:04X}".format(error_status))
            error_status = self.motorRB.get_error_status()
        if error_status == 0x0000:
            print("Speed R:", self.motorRB.speed) # If no error, print speed
        else:
            print("Error status: 0x{:04X}".format(error_status))
        error_status = self.motorL.get_error_status()
        if error_status == 0x0000:
            print("Speed L:", self.motorL.speed) # If no error, print speed
        else:
            print("Error status: 0x{:04X}".format(error_status))
 
    # Handle Keyboard Interupts
    def start_keyboard_control(self):
        keyboard.on_press(self.handle_key_event)
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()
 
# Main Procedure
def main():
 
    # DECLARATIONS
    # Motor Right on address 11
    MotorR = SmcG2I2C(SMBus(11), 16) # PINS Bus , Address
 
    # Motor Right Back on address 17
    MotorRB = SmcG2I2C(SMBus(11), 17) # PINS Bus , Address
 
    # Motor Left on bus address
    MotorL = SmcG2I2C(SMBus(11), 15) # PINS Bus , Address
 
    # Motor Left Back doesn't exist
    # ------------
 
    # INTIALIZATION
 
    # motorR startup
    MotorR.exit_safe_start()
    error_status = MotorR.get_error_status()
    if error_status == 0x0000:
        print("Right Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
 
    # motorRB startup
    MotorRB.exit_safe_start()
    error_status = MotorRB.get_error_status()
    if error_status == 0x0000:
        print("Right Motor Back Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
 
    # motorL startup
    MotorL.exit_safe_start()
    error_status = MotorL.get_error_status()
    if error_status == 0x0000:
        print("Left Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
    # --- END INITIALIZATION---  
 
 
    # Keyboard Control Loop
    control_interface = KeyboardControlInterface(MotorL, MotorR, MotorRB)
    control_interface.start_keyboard_control()
    # need to create some exit code...
 
# Python Convention!
# If this is the main program root, run main loop
# Otherwise, if it's being imported as a module, just expose its methods
if __name__ == "__main__":
    main()
 
 
 
 
 
# 
 
# HOW TO INSTALL:
# install smbus2 and keyboard libraries with
# sudo pip3 install <libraries>
# - access to the keyboard requires root level Operating System access
# this is why we need to install our Python packages using sudo
 
 
# ::: DOCUMENTATION :::
 
# ERRORS:
# There was an error caused by rate of inputting speed, it went away on Day 2
# ????
 
# 1. Can't switch directions at max speed
#     - from 3200 to -3200
#       possibly the range???
#       some acelleration algorithim
 
# Some relationship between range of speed difference and
# Rate of toggling
# -2800 to 2800 causes error at rapid toggling
# Wires may have some load
 
 
 
# POLULU DOCUMENTATION:
# Uses the smbus2 library to send and receive data from a
# Simple Motor Controller G2.
# Works on Linux with either Python 2 or Python 3.
#
# NOTE: The SMC's input mode must be "Serial/USB".
# NOTE: You might need to change the 'SMBus(3)' line below to specify the
#   correct I2C bus device.
# NOTE: You might need to change the 'address = 13' line below to match
#   the device number of your Simple Motor Controller.
