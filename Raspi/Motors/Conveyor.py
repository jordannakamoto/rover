# ------------------------------------------------------------------------------- #
# Conveyor Controller
# class for controling a pair of motors - although we are only interested in one
# TODO: Refactor library source code to only instance a single motor instead of a pair
# 
# SOURCE: https://github.com/pololu/dual-g2-high-power-motor-driver-rpi
# ------------------------------------------------------------------------------- #

from dual_g2_hpmd_rpi import motors, MAX_SPEED

class G2Conveyor:
    def __init__(self):
        motors.setSpeeds(0, 0)      # Before setting speed, init to 0. Even though we only use 1 motor, the library code is programmed for 2
        print("Conveyor Init")
        self.conveyor_speed = -475  # Reverse direction needd
        self.conveyor_is_on = False # Flag
        

    # -- Simple Start and Stop -- #
    def start_conveyor(self):
        print("Entering startConveyor")
        motors.motor1.setSpeed(self.conveyor_speed)
        self.conveyor_is_on = True

    def stop_conveyor(self):
        motors.motor1.setSpeed(0)
        self.conveyor_is_on = False


# ------------------------------------------------------------------------------- #