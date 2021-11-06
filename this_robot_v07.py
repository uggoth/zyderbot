import utime
import collections
import motor_pins_pwm_v01 as motor_pins
Pin = motor_pins.Pin
PWM = motor_pins.PWM

class DriveTrainL298N():

    #  speed is from -100 (full astern) through 0 (stop) to +100 (full ahead)
    #  smoothness is no. of milliseconds to get up to speed

    def __init__(self):

        pin_list = motor_pins.MotorPins()

        self.all_motors = [pin_list.right_front_fwd, pin_list.left_front_fwd, pin_list.right_rear_fwd, pin_list.left_rear_fwd,
                           pin_list.right_front_rev, pin_list.left_front_rev, pin_list.right_rear_rev, pin_list.left_rear_rev]

        self.fwd = [pin_list.right_front_fwd, pin_list.left_front_fwd, pin_list.right_rear_fwd, pin_list.left_rear_fwd]
        self.rev = [pin_list.right_front_rev, pin_list.left_front_rev, pin_list.right_rear_rev, pin_list.left_rear_rev]
        self.spr = [pin_list.right_front_rev, pin_list.left_front_fwd, pin_list.right_rear_rev, pin_list.left_rear_fwd]
        self.spl = [pin_list.right_front_fwd, pin_list.left_front_rev, pin_list.right_rear_fwd, pin_list.left_rear_rev]

        self.left_fwd = [pin_list.left_front_fwd, pin_list.left_rear_fwd]
        self.right_fwd = [pin_list.right_front_fwd, pin_list.right_rear_fwd]
        self.left_rev = [pin_list.left_front_rev, pin_list.left_rear_rev]
        self.right_rev = [pin_list.right_front_rev, pin_list.right_rear_rev]

        self.max_duty = 65536
        self.min_duty = 6554
        
        self.current_left_speed_percent = 0
        self.current_right_speed_percent = 0
        self.acceleration_steps = 20

    def set_motors(self, train, percent):
        if percent == 0:
            duty = 0
        else:
            duty = self.min_duty + int(((self.max_duty - self.min_duty) * percent) / 100)
        for motor in train:
            motor.duty_u16(duty)

    def set_side(self, side, percent):
        print (side, percent)
        if (percent < 0) and (side =='L'):
            self.set_motors(self.left_rev, -percent)
        elif (percent > 0) and (side =='L'):
            self.set_motors(self.left_fwd, percent)
        elif (percent < 0) and (side =='R'):
            self.set_motors(self.right_rev, -percent)
        elif (percent > 0) and (side =='R'):
            self.set_motors(self.right_fwd, percent)
        elif side == 'R':
            self.set_motors(self.right_fwd, 0)
            self.set_motors(self.right_rev, 0)
        elif side == 'L':
            self.set_motors(self.left_fwd, 0)
            self.set_motors(self.left_rev, 0)
        else:
            self.set_motors(self.all_motors, 0)
            
        if side == 'L':
            self.current_left_speed_percent = percent
        else:
            self.current_right_speed_percent = percent

    def drive(self, command_tuple):
        target_left_speed_percent = command_tuple[0]  # from -100 (max rev) to 0 (stopped) to +100 (max fwd)
        target_right_speed_percent = command_tuple[1]
        smoothness = command_tuple[2]  # milliseconds to get to speed
        if smoothness > 0:
            delay = int(smoothness / self.acceleration_steps)
            left_delta = (target_left_speed_percent - self.current_left_speed_percent) / self.acceleration_steps
            right_delta = (target_right_speed_percent - self.current_right_speed_percent) / self.acceleration_steps
            for i in range(self.acceleration_steps):
                next_left_speed_percent = self.current_left_speed_percent + left_delta
                next_right_speed_percent = self.current_right_speed_percent + right_delta
                self.set_side('L', next_left_speed_percent)
                self.set_side('R', next_right_speed_percent)
                utime.sleep_ms(delay)
        self.set_side('L', target_left_speed_percent)
        self.set_side('R', target_right_speed_percent)

    def accelerate(self, train, to_speed, angle, acceleration):
        speed_delta = to_speed - self.current_speed
        increment = int((to_speed - self.current_speed) / self.acceleration_increments) + 1
        for duty in range(start_speed, end_speed, increment):
            for motor in train:
                motor.duty_u16(duty)
            utime.sleep_ms(sleep_interval)
       
class ThisRobot():

    def __init__(self):

        self.inputs = {}
        self.inputs['YELLOW_BUTTON'] = {'PIN':Pin(26, Pin.IN, Pin.PULL_UP),
                                        'NAME':'Yellow Button',
                                        'STATE':'UNKNOWN'}
        self.inputs['GREEN_BUTTON'] = {'PIN':Pin(27, Pin.IN, Pin.PULL_UP),
                                        'NAME':'Green Button',
                                        'STATE':'UNKNOWN'}
        #  NOTE: Blue button directly connected to pin 30 (RESET)
        #self.inputs['BLUE_BUTTON'] = {'PIN':Pin(2, Pin.IN, Pin.PULL_UP),
        #                                'NAME':'Blue Button',
        #                                'STATE':'UNKNOWN'}

        self.drive_train = DriveTrainL298N()
