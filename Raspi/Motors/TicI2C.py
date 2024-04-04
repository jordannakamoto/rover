# ----------------------------------------------------------------
# Class for Belt Stepper and Dump Bucket
# Sourced from Pololu
# Created by Josh
# https://www.pololu.com/docs/0J71/12.9
# ----------------------------------------------------------------
import time
from smbus2 import i2c_msg
import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class TicI2C(object):  
  
  # Bus passed by argument
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
  def set_target_position(self, target):
    target = int(target)
    command = [0xE0,
      target >> 0 & 0xFF,
      target >> 8 & 0xFF,
      target >> 16 & 0xFF,
      target >> 24 & 0xFF]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)

  # set target_velocity
  def set_target_velocity(self, target):
    target = int(target)
    command = [0xE3,
      target >> 0 & 0xFF,
      target >> 8 & 0xFF,
      target >> 16 & 0xFF,
      target >> 24 & 0xFF]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)

  # jordan added
  def emergency_stop(self):
     self.set_target_velocity(0)
     print("Emergency stop activated!")
    
  def homeFwd(self):
    command = [0x97, 0x01]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
    
  def homeRev(self):
    command = [0x97, 0x00]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
    
  def move_cm(self, distance_down):
        cm_to_steps = 16000/2.5
        linear_distance = distance_down / math.sin(math.radians(self.angle))
        steps = linear_distance * cm_to_steps
        targetPosition = self.position + steps
        self.set_target_position(targetPosition)
        self.position = targetPosition
 