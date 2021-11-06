from machine import Pin, PWM

class MotorPins:
    
    def __init__(self):
        self.right_front_rev = PWM(Pin(20))
        self.right_front_fwd = PWM(Pin(21))
        self.left_front_rev = PWM(Pin(19))
        self.left_front_fwd = PWM(Pin(18))
        self.right_rear_rev = PWM(Pin(12))
        self.right_rear_fwd = PWM(Pin(13))
        self.left_rear_rev = PWM(Pin(11))
        self.left_rear_fwd = PWM(Pin(10))

