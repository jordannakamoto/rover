# ------------------------------------------------------------------------------- #
# Conveyor Controller
# class for controling a pair of motors - although we are only interested in one
# TODO: Refactor library source code to only instance a single motor instead of a pair
# 
# SOURCE: https://github.com/pololu/dual-g2-high-power-motor-driver-rpi
# ------------------------------------------------------------------------------- #

from dual_g2_hpmd_rpi import motors, MAX_SPEED

class G2ConveyorMotor:
    def __init__(self):
        self.conveyor_speed = 470
        self.conveyor_is_on = False
        motors.setSpeeds(0, 0)
        # Even though we only use 1 motor, the library code is programmed for 2
        # On the insantiation of the motor Interface, make sure to set both speeds to 0

    # -- Simple Start and Stop -- #
    def start_conveyor(self):
        print("Entering startConveyor")
        motors.motor1.setSpeed(self.conveyor_speed)
        self.conveyor_is_on = True

    def stop_conveyor(self):
        motors.motor1.setSpeed(0)
        self.conveyor_is_on = False




# ------------------------------------------------------------------------------- #
# Unused Fault Event Handling
# class DriverFault(Exception):
#     def __init__(self, driver_num):
#         super().__init__(f"Driver {driver_num} fault!")
#         self.driver_num = driver_num
# 
# def raise_if_fault(self):
#     if motors.motor1.getFault():
#         raise self.DriverFault(1)