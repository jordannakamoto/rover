import time
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
import math

cm_to_steps = 16000/2.5

GPIO.setmode(GPIO.BCM)
#GPIO.setup(HOME_LIMIT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class TicI2C(object):
  def __init__(self, bus, address, angle):
    self.bus = bus
    self.address = address
    self.angle = angle
    self.position = 0
 
  # Sends the "Exit safe start" command.
  def exit_safe_start(self):
    command = [0x83]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
 
  # Sets the target position.
  #
  # For more information about what this command does, see the
  # "Set target position" command in the "Command reference" section of the
  # Tic user's guide.
  def set_target_position(self, target):
    target = int(target)
    command = [0xE0,
      target >> 0 & 0xFF,
      target >> 8 & 0xFF,
      target >> 16 & 0xFF,
      target >> 24 & 0xFF]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)


  def set_target_velocity(self, target):
    target = int(target)
    command = [0xE3,
      target >> 0 & 0xFF,
      target >> 8 & 0xFF,
      target >> 16 & 0xFF,
      target >> 24 & 0xFF]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
    
  def homeFwd(self):
    command = [0x97, 0x01]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
    
  def homeRev(self):
    command = [0x97, 0x00]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
    
  def move_cm(self, distance_down):
        linear_distance = distance_down / math.sin(math.radians(self.angle))
        steps = linear_distance * cm_to_steps
        targetPosition = self.position + steps
        self.set_target_position(targetPosition)
        self.position = targetPosition
 
    
# Open a handle to "/dev/i2c-3", representing the I2C bus.
bus = SMBus(1)

# Bus, Address, Angle (for computing step distance in cm)
motor = TicI2C(bus, 16, 90)

#reverse belt stepper to start position
motor.homeRev()

#main loop
while True:
    print("a = home fwd\n d = home rev\n w = move fwd\n s = move back\n")
    x = input()
    if (x=='a'):
        motor.homeRev()
    elif (x== 'd'):
        motor.homeFwd()
    elif (x == 'w'):
        motor.move_cm(1)
    elif (x == 's'):
        motor.move_cm(-1)
    time.sleep(0.01)
