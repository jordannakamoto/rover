# Conveyor1
# Script Executable from Raspi over SSH to just spin a motor on the piHat connection
# To stop the conveyor from spinning, just exit the script


import signal
import sys
import time
from smbus2 import SMBus, i2c_msg
#import RPi.GPIO as GPIO
import math


#jordan imports
from dual_g2_hpmd_rpi import motors, MAX_SPEED

# end imports

# global variables
conveyor_speed = 470
conveyorIsOn = False

# ---- Start Jordan Code  -------
    
class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

# After you set the speeds, you can throw a fault check
def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)

def startConveyor():
    print("Entering startConveyor")
    

def stopConveyor():
    motors.motor1.setSpeed(0)
        
# HANDLE PROGRAM EXIT 
def cleanup_and_exit(signal_received, frame):
    stopConveyor()  # Ensure the conveyor is stopped
    print("\nExiting gracefully")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, cleanup_and_exit)

# Start of main combined
def main():
    try:
        motors.setSpeeds(0, 0)
        motors.motor1.setSpeed(480)

        # print("Motor 1 forward")
        
        # while True:
        #     user_input = input("Enter your input:")
        #     if user_input == "1":
        #         motors.motor1.setSpeed(480)
        #     elif user_input == "2":
        #         motors.motor1.setSpeed(0)
            
            # Note: This creates an infinite loop, preventing any further code from running,
            # including catching exceptions. You might want to reconsider this logic.
        while True:
            continue

    except DriverFault as e:
        print(f"Driver {e.driver_num} fault!")

main()




