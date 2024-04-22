import time
from smbus2 import SMBus, i2c_msg
import RPi.GPIO as GPIO
from Motors import TicI2C

GPIO.setmode(GPIO.BCM)

bus = SMBus(1)
motor = TicI2C

print("motor: \n 1. conveyorArm \n 2. dumpBucket \n 3. dumpSlide")
x = input()
if(x=='1'):
    motor = TicI2C(bus, 15, 45)
    print("testing conveyorArm motor")
elif (x=='2'):
    motor = TicI2C(bus,14, 90)
    print("testing dumpBucket motor")
elif (x=='3'):
    motor = TicI2C(bus,16, 90)
    print("testing dumpSlide motor")

#main loop
while True:
    
    print("a = extend\n d = retract hone\n w = move fwd\n s = move back\n")
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