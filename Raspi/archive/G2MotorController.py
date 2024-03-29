from smbus2 import SMBus, i2c_msg
 
# MOTOR DEFINITIONS
# |  class
# |  G2MotorController
# |  Simple Motor Controller G2 I2C Interface  
# |  https://www.pololu.com/docs/0J77/all
# |  usage: Object to control a single Pololu G2I2C motor
class G2MotorController(object): # TODO: give name to motor class

  acceleration = 100  # Adjust as needed
  deceleration_factor = 0.8  # Adjust as needed

  ### Initialization ###
  def __init__(self, name, bus, address, debug):
    self.name = name
    self.bus = bus
    self.address = address
    self.current_speed = 0 # Tracking speed of the motor... Pololu also supports a reading directly from the Pin (Line 101) but I'm not sure which is prefferable - Jordan

    # Optional Debug Metrics:
    if debug:
            self.isDebugMode = True
            self.target_speed_debug = 0
            self.acceleration_factor_debug = 0
            self.deceleration_factor_debug = 0
            self.acceleration_rate_debug = 0
            self.deceleration_rate_debug = 0
            self.print_debug_values_periodically(1)
    else:
            self.isDebugMode = False
            self.target_speed_debug = None
            self.acceleration_factor_debug = None
            self.deceleration_factor_debug = None
            self.acceleration_rate_debug = None
            self.deceleration_rate_debug = None

  def print_debug_values_periodically(self, interval):
        while True:
            print("Debug ", self.name)
            print("Current Speed:", self.current_speed)
            print("Target Speed :", self.target_speed_debug)
            print("Acc Factor   :", self.acceleration_factor_debug)
            print("Acc Rate     :", self.acceleration_rate_debug)
            print("Dec Factor   :", self.deceleration_factor_debug)
            print("Dec Rate     :", self.deceleration_rate_debug)
            time.sleep(interval)


  # Sends the Exit Safe Start command, which is required to drive the motor.
  def exit_safe_start(self):
    write = i2c_msg.write(self.address, [0x83])
    self.bus.i2c_rdwr(write)
  ###
 
  ### Speed Control Methods ###
  # Sets the SMC's target speed (-3200 to 3200).
  def write_speed(self, speed):
    cmd = 0x85  # Motor forward > cmd stores the direction code for the motor
    if speed < 0:
      cmd = 0x86  # Motor reverse
      speed = -speed
    buffer = [cmd, speed & 0x1F, speed >> 5 & 0x7F]
    write = i2c_msg.write(self.address, buffer)
    self.bus.i2c_rdwr(write)
 
  # Accelerate
  def accelerate(self, current_speed, target_speed):
    if current_speed == target_speed:
        return current_speed

    acceleration_factor = self.acceleration / 3200  # Normalize to [-1, 1]

    sigmoid_input = 2 * (current_speed - target_speed) / 3200  # Normalize to [-1, 1]
    acceleration = 3200 * (1 / (1 + math.exp(-sigmoid_input))) * acceleration_factor

    #Debug
    acceleration_factor_debug = acceleration_factor
    acceleration_rate_debug = acceleration

    return current_speed + acceleration

  # Decelerate
  def decelerate(self, current_speed, target_speed):
      if current_speed == target_speed:
          return current_speed

      deceleration_factor = self.deceleration_factor

       # Metrics Debug
      deceleration_factor_debug = deceleration_factor

      sigmoid_input = 2 * (current_speed - target_speed) / 3200  # Normalize to [-1, 1]
      deceleration = 3200 * (1 / (1 + math.exp(-sigmoid_input))) * deceleration_factor

      #Debug
      deceleration_factor_debug = deceleration_factor
      deceleration_rate_debug = deceleration

      return current_speed - deceleration

  # SET TARGET SPEED
  # Utilizes acceleration and deceleration curves
  # Range: -3200 to 3200
  def set_target_speed(self, target_speed):
        target_speed = max(-3200, min(target_speed, 3200))  # Limit speed to valid range
        target_speed = int(target_speed)
        
        #Debug
        target_speed_debug = target_speed

        # if greater than, use accelleration curve
        while self.current_speed != target_speed:
            if target_speed >= self.current_speed:
                self.current_speed = self.accelerate(self.current_speed, target_speed)
            else:
                self.current_speed = self.decelerate(self.current_speed, target_speed)

            self.write_speed(self.current_speed)
            time.sleep(0.1)  # Feed new speed every 0.1 seconds
  ###

  # Gets the specified variable as an unsigned value.
  def get_variable(self, id):
    write = i2c_msg.write(self.address, [0xA1, id])
    read = i2c_msg.read(sef.address, 2)
    self.bus.i2c_rdwr(writel, read)
    b = list(read)
    return b[0] + 256 * b[1]
 
  # Gets the specified variable as a signed value.
  def get_variable_signed(self, id):
    value = self.get_variable(id)
    if value >= 0x8000:
      value -= 0x10000
    return value
 
  # Gets the target speed (-3200 to 3200).
  def get_target_speed(self):
    return self.get_variable_signed(20)
 
  # Gets a number where each bit represents a different error, and the
  # bit is 1 if the error is currently active.
  # See the user's guide for definitions of the different error bits.
  def get_error_status(self):
    return self.get_variable(0)
