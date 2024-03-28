# Keyboard Controller
SPEED_OF_CONVEYOR_MOTOR = 2800
 
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
# |  motor 1
# |  Spins one motor forward with w and and reverse direction with s
class KeyboardControlInterface(object):

    def __init__(self, motor1):
        self.motor1 = motor1
 
    # --- Handling --- #
    def handle_key_event(self, event):
        key = event.name
 
        # key w | Spin Motor
        if key == 'w': 
            self.motor1.speed = SPEED_OF_CONVEYOR_MOTOR
            # set new speeds on Right and Left motors
            new_speed = self.motor1.speed * self.motor1.direction
            self.motor1.set_target_speed(new_speed)
        # key s | Reverse
        elif key == 's':
            self.motor1.set_target_speed(0) # Set speed to 0 before reversing
            self.motor1.direction *= -1
            #  Resend Speed with new direction information
            self.motor1.speed = SPEED_OF_CONVEYOR_MOTOR
            new_speed = self.motor1.speed * self.motor1.direction
        else: # Optional TODO: Add an exit option...
            return

        # At end of every command issued, Error Reporting
        error_status = self.motor1.get_error_status()
        if error_status == 0x0000:
            print("Speed R:", self.motor1.speed) # If no error, print speed
        else:
            print("Error status: 0x{:04X}".format(error_status))

    # --- Loop for recognizing Events for Key (Press) then send to Handler ---
    def start_keyboard_control(self):
        keyboard.on_press(self.handle_key_event)
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()
 
# --- Main Procedure ---
def main():
 
    # Motor Hardware Definition
    Motor1 = SmcG2I2C(SMBus(11), 16) # PINS Bus , Address
    # ------------
 
    # Initialize Motor on I2C Bus
    Motor1.exit_safe_start()
    error_status = Motor1.get_error_status()
    if error_status == 0x0000:
        print("Right Motor Ready!")
    else:
        print("Error status: 0x{:04X}".format(error_status))
 
    # Start Keyboard Control Loop
    control_interface = KeyboardControlInterface(Motor1)
    control_interface.start_keyboard_control()
    # need to create some exit code...
 
# Python Convention!
# If this is the main program root, run main loop
# Or if it's imported as a module, don't invoke main loop
if __name__ == "__main__":
    main()
 
 