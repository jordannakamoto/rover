import time
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
import math
import subprocess


# end imports

# global variables

cm_to_steps = 16000/2.5
conveyor_process = None

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

# ---- Start Jordan Code  -------
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

# Start of main combined
    
# Open a handle to "/dev/i2c-3", representing the I2C bus.
bus = SMBus(1)

beltStep = TicI2C(bus, 15, 45)
dumpBucket = TicI2C(bus,14, 90)
#reverse belt stepper to start position
beltStep.homeRev()
#reverse bucket to start position
#dumpBucket.homeRev()

# init conveyor
conveyorIsOn = False

#main loop
while True:
    x = input()
    if (x == 'w'):
        beltStep.move_cm(1)
    if (x == 's'):
        beltStep.move_cm(-1)
    if (x == 'a'):
        dumpBucket.move_cm(1)
    if (x == 'd'):
        dumpBucket.move_cm(-1)
    if (x == 'o'): # start/stop conveyor motor spinning program
        toggle_conveyor_operation()
    
    time.sleep(0.01)

