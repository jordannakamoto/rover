from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import keyboard

class DriverFault(Exception):
    def __init__(self, driver_num):
        self.driver_num = driver_num

def raiseIfFault():
    if motors.motor1.getFault():
        raise DriverFault(1)
    if motors.motor2.getFault():
        raise DriverFault(2)

def move_motor(direction):
    motors.setSpeeds(0, 0)  # Initialize speeds to 0.
    
    if direction == "forward":
        speeds = list(range(0, MAX_SPEED, 10)) + [MAX_SPEED] * 100 + list(range(MAX_SPEED, 0, -10)) + [0]
    elif direction == "reverse":
        speeds = list(range(0, -MAX_SPEED, -10)) + [-MAX_SPEED] * 100 + list(range(-MAX_SPEED, 0, 10)) + [0]
    else:
        print("Unknown direction!")
        return
    
    for speed in speeds:
        try:
            motors.motor1.setSpeed(speed)
            motors.motor2.setSpeed(speed)
            raiseIfFault()
            time.sleep(0.002)
        except DriverFault as e:
            print("Driver %s fault!" % e.driver_num)
            break

def on_press(event):
    if event.name == 'w':
        print("Moving forward")
        move_motor("forward")
    elif event.name == 's':
        print("Reversing")
        move_motor("reverse")

def main():
    keyboard.on_press(on_press)
    
    try:
        print("Press 'w' to move forward, 's' to reverse. Press 'Ctrl+C' to exit.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program exited.")
    finally:
        motors.forceStop()
        keyboard.unhook_all()

if __name__ == "__main__":
    main()
