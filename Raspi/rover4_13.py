import time
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
import math
import subprocess
import termios
import tty
import os
import sys

# --------------------------------------------------------- #
# Homing methods... move until limit switch is hit
# Function HomeFwd - extends I2C from physical motor base
# Function HomeRev - retracts I2C back to base (home)
# --------------------------------------------------------- #e es

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

# Launch/Terminate subprocess for conveyor on/off
def toggle_conveyor_operation():
  global conveyor_process

  if conveyor_process:
      print("Stopping conveyor...")
      conveyor_process.terminate()  # Terminate the process
      conveyor_process.wait()  # Wait for process to terminate
      conveyor_process = None
  else:
      print("Starting conveyor...")
      conveyor_process = subprocess.Popen(['python3', 'conveyor1.py'])

# Procedure to ensure the conveyor isn't running during other operations
def kill_conveyor():
  global conveyor_process

  if conveyor_process:
      print("Stopping conveyor...")
      conveyor_process.terminate()  # Terminate the process
      conveyor_process.wait()       # Wait for process to terminate
      conveyor_process = None

# Flush stdin to clear unwanted inputs so we can't button mash
def flush_input():
    try:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH) # For Unix/Linux systems.
    except Exception as e:
        print("Flush not supported on this platform.")

def print_instructions():
   # Print Instructions
  print("Instructions:")
  print("'w' - Move belt arm down 1 cm")
  print("'s' - Move belt arm up 1 cm")
  print("'j' - Home belt arm")
  print("'o' - Toggle conveyor")
  print("'d' - Dump Bucket")
  print("'a' - Reset Bucket")
  print("'0' - Quit")
  print("--------------------------------------------\n")

def print_status():
  global beltPosition
  global isDumpComplete
  # Print Status
  if(beltPosition == 0):
      print("Belt Arm: home")
  else:
      print("Belt Arm: +%0.2f cm", beltPosition)
  if(conveyor_process):
      print("Conveyor: ON")
  else:
      print("Conveyor: off") 
  if(isDumpComplete):
      print("Dump Bucket: COMPLETED dump!")
  else:
      print("Dump Bucket: collection position...")

# Open a handle to "/dev/i2c-3", representing the I2C bus.
bus = SMBus(1)

beltStep = TicI2C(bus, 15, 45)
dumpBucket = TicI2C(bus,14, 90)

# Adding dumpSlide to slide the dump bucket closer to the conveyor drop off
dumpSlide = TicI2C(bus, 16, 90)

# INIT by homing
#reverse belt stepper to start position
beltStep.homeRev()
#reverse bucket to start position
dumpBucket.homeRev()
#reverse dump slide to start position
dumpSlide.homeRev()

beltPosition = 0              # 0 for home
belt_move_duration   = 1      # in seconds
dump_slide_duration  = 10     # TODO: Time slide duration
dump_homing_duration = 17.54

isDumpComplete = False       # flag to indicate if dump is complete

#main loop
while True:
    print_instructions()
    # get input
    x = input()
    action_time = time.time()
    if (x == 'w'):
        beltStep.move_cm(1)
        beltPosition += 1
        time.sleep(belt_move_duration)
    elif (x == 's'):
        if(beltPosition == 0):
           print("Belt is already at home, cant step up...")
           continue
        beltStep.move_cm(-1)
        beltPosition -= 1
        time.sleep(belt_move_duration)
    elif (x == 'j'):
        beltStep.homeRev()
        beltPosition = 0
        kill_conveyor()
        time.sleep(belt_move_duration * beltPosition)
    # ! a and d: TODO double check dumpslide homeRev/homeFwd
    elif (x == 'd'):
        os.system('clear') # clear the screen
        kill_conveyor()
        print("Sliding to dump position...")
        dumpSlide.homeFwd()
        time.sleep(dump_slide_duration)
        print("Starting dump...")
        dumpBucket.homeFwd()
        time.sleep(dump_homing_duration)
        isDumpComplete = True
    elif (x == 'a'):
        os.system('clear')
        kill_conveyor()
        isDumpComplete = False
        print("Retracting dump bucket back to home...")
        dumpBucket.homeRev()
        time.sleep(dump_homing_duration)
        print("Sliding back to collection position...")
        dumpSlide.homeRev()
        time.sleep(dump_slide_duration)
    elif (x == 'o'):
        toggle_conveyor_operation()
    elif (x == '0'):
        kill_conveyor()
        time.sleep(2)
        exit()

    flush_input()
    os.system('clear') # clear the screen
    print("Ready")
    time.sleep(0.01)