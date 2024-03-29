class ConveyorController:
    def __init__(self):
        self.conveyor_speed = 470
        self.conveyor_is_on = False
        signal.signal(signal.SIGINT, self.cleanup_and_exit)

    class DriverFault(Exception):
        def __init__(self, driver_num):
            super().__init__(f"Driver {driver_num} fault!")
            self.driver_num = driver_num

    def raise_if_fault(self):
        if motors.motor1.getFault():
            raise self.DriverFault(1)

    def start_conveyor(self):
        print("Entering startConveyor")
        motors.motor1.setSpeed(self.conveyor_speed)
        self.conveyor_is_on = True

    def stop_conveyor(self):
        motors.motor1.setSpeed(0)
        self.conveyor_is_on = False

    def cleanup_and_exit(self, signal_received, frame):
        self.stop_conveyor()  # Ensure the conveyor is stopped
        print("\nExiting gracefully")
        sys.exit(0)

    def run(self):
        try:
            motors.setSpeeds(0, 0)  # Initialize motors to 0 speed
            self.start_conveyor()   # Start the conveyor

            while True:
                # Your loop or logic here. This example will just run indefinitely.
                # You can add conditions or inputs to modify the behavior.
                time.sleep(1)  # Placeholder to simulate ongoing process
        except self.DriverFault as e:
            print(e)