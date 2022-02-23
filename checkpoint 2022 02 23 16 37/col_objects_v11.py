#  Useful Objects from Colin Walls

from machine import Pin, PWM
import utime
import math
#from i2c_slave_v03 import i2c_slave

class CommandStream():
    
    def __init__(self, i2c_s):
        self.i2c_s = i2c_s

    def split(self, num):
        num0 = num % 65536
        numb = num0 % 256
        numa = int((num0 - numb) / 256)
        return numa, numb

    def get(self):
        command_array = []
        command_length = 9
        for i in range(command_length):
            command_byte = self.i2c_s.get()  #  blocking?
            command_array.append(command_byte)
        command_code = chr(command_array[0])
        par_1 = (command_array[1] * 256) + command_array[2]
        par_2 = (command_array[3] * 256) + command_array[4]
        par_3 = (command_array[5] * 256) + command_array[6]
        par_4 = (command_array[7] * 256) + command_array[8]
        return command_code, par_1, par_2, par_3, par_4
    
    def send(self,array):
        return self.i2c_s.slave_transmit(array)

class ir_sensor():
    def __init__(self, pin, pin_level, irq_callback):
        self.name = 'Unknown'
        self.pin = pin
        self.pin_level = pin_level
        self.irq_callback = irq_callback
        #  parms will be: pin, pin_level, value
        #  -- EXAMPLE --
        #  def my_callback(pin, pin_level, value):
        #      print (pin, pin_level, value)
        #      return True   #  if want IRQ left off
        self.pin.irq(trigger=pin_level, handler=self.event_occured)

    def event_occured(self, device):
        device.irq(handler=None)
        utime.sleep_us(10)   # debounce
        value_1 = device.value()
        utime.sleep_us(50)
        value_2 = device.value()
        if value_1 == value_2:
            if self.irq_callback(self, value_2):
                return
        device.irq(trigger=self.pin_level, handler=self.event_occured)
    
    def close(self):
        self.pin.irq(handler=None)

class BackIRArriving(ir_sensor):
    def __init__(self, irq_callback):
        super().__init__(Pin(18, Pin.IN, Pin.PULL_UP), Pin.IRQ_FALLING, irq_callback)
        self.name = "Back IR Arriving"
        
class FrontIRArriving(ir_sensor):
    def __init__(self, irq_callback):
        super().__init__(Pin(22, Pin.IN, Pin.PULL_UP), Pin.IRQ_FALLING, irq_callback)
        self.name = "Front IR Arriving"
        
class BackIRDeparting(ir_sensor):
    def __init__(self, irq_callback):
        super().__init__(Pin(18, Pin.IN, Pin.PULL_UP), Pin.IRQ_RISING, irq_callback)
        self.name = "Back IR Departing"
        
class FrontIRDeparting(ir_sensor):
    def __init__(self, irq_callback):
        super().__init__(Pin(22, Pin.IN, Pin.PULL_UP), Pin.IRQ_RISING, irq_callback)
        self.name = "Front IR Departing"
        

class FIT0441():
    
    def __init__(self, direction_pin, speed_pin, pulse_pin):
        self.direction_pin = direction_pin
        self.speed_pin = speed_pin
        self.pulse_pin = pulse_pin
        self.pulse_pin.irq(self.pulse_detected)
        self.pulse_count = 0
        self.stop_duty = 65534
        self.min_speed_duty = 45000
        self.max_speed_duty = 0
        self.clockwise = 1
        self.anticlockwise = 0
        self.name = 'Unknown'

    def deinit(self):
        self.speed_pin.deinit()

    def stop(self):
        duty = self.stop_duty
        self.speed_pin.duty_u16(duty)

    def pulse_detected(self, sender):
        self.pulse_count += 1

    def get_pulses(self):
        return self.pulse_count

    def set_speed(self, speed):  #  as a percentage
        duty = self.min_speed_duty - int(float(self.min_speed_duty - self.max_speed_duty) * float(speed) / 100.0)
        #print (speed,duty)
        self.speed_pin.duty_u16(duty)
    
    def set_direction(self, direction):  # 1 = clockwise, 0 = anticlockwise
        if direction == 1:
            self.direction_pin.value(self.clockwise)
        elif direction == 0:
            self.direction_pin.value(self.anticlockwise)
            
class DriveTrain():
    
    def __init__(self, left_motor_list, right_motor_list):
        self.left_motor_list = left_motor_list
        self.right_motor_list = right_motor_list
    
    def drive(self, angle_in, speed_in):
        angle = angle_in % 360
        if angle < 90:
            for motor in self.left_motor_list:
                motor.set_direction(0)
                speed = speed_in
                motor.set_speed(speed_in)
            for motor in self.right_motor_list:
                if angle < 45:
                    motor.set_direction(1)
                    speed = int(speed_in * ((45 - angle) / 45))
                else:
                    motor.set_direction(0)
                    speed = int(speed_in * ((angle - 45) / 45))
                motor.set_speed(speed)
            return True
        elif angle < 180:
            for motor in self.left_motor_list:
                if angle < 135:
                    motor.set_direction(0)
                    speed = int(speed_in * ((135 - angle) / 135))
                else:
                    motor.set_direction(1)
                    speed = int(speed_in * ((angle - 135) / 135))
                motor.set_speed(speed)
            for motor in self.right_motor_list:
                motor.set_direction(0)
                speed = speed_in
                motor.set_speed(speed)
            return True
        elif angle < 270:
            for motor in self.left_motor_list:
                motor.set_direction(1)
                speed = speed_in
                motor.set_speed(speed)
            for motor in self.right_motor_list:
                if angle < 225:
                    motor.set_direction(0)
                    speed = int(speed_in * ((225 - angle) / 225))
                else:
                    motor.set_direction(1)
                    speed = int(speed_in * ((angle - 225) / 225))
                motor.set_speed(speed)
            return True
        elif angle < 360:
            for motor in self.left_motor_list:
                if angle < 315:
                    motor.set_direction(1)
                    speed = int(speed_in * ((315 - angle) / 315))
                else:
                    motor.set_direction(0)
                    speed = int(speed_in * ((angle - 315) / 315))
                motor.set_speed(speed)
            for motor in self.right_motor_list:
                motor.set_direction(1)
                speed = speed_in
                motor.set_speed(speed)
            return True
        else:
            print ('**** bad angle *****')
            return False
    
    def pulses_to_millimetres(self, pulses):
        return int(pulses * 300 / 505)

    def stop(self):
        for motor in self.left_motor_list:
            motor.stop()
        for motor in self.right_motor_list:
            motor.stop()

class ThisDriveTrain(DriveTrain):

    def __init__(self):

        self.lf_speed_pin = PWM(Pin(2))
        self.lf_direction_pin = Pin(4, Pin.OUT)
        self.lf_pulse_pin = Pin(3, Pin.IN, Pin.PULL_UP)
        self.motor_lf = FIT0441(self.lf_direction_pin, self.lf_speed_pin, self.lf_pulse_pin)
        self.motor_lf.name = 'Left Front'

        self.rf_speed_pin = PWM(Pin(6))
        self.rf_direction_pin = Pin(8, Pin.OUT)
        self.rf_pulse_pin = Pin(7, Pin.IN, Pin.PULL_UP)
        self.motor_rf = FIT0441(self.rf_direction_pin, self.rf_speed_pin, self.rf_pulse_pin)
        self.motor_rf.name = 'Right Front'

        self.lb_speed_pin = PWM(Pin(10))
        self.lb_direction_pin = Pin(11, Pin.OUT)
        self.lb_pulse_pin = Pin(12, Pin.IN, Pin.PULL_UP)
        self.motor_lb = FIT0441(self.lb_direction_pin, self.lb_speed_pin, self.lb_pulse_pin)
        self.motor_lb.name = 'Left Back'

        self.rb_speed_pin = PWM(Pin(21))
        self.rb_direction_pin = Pin(20, Pin.OUT)
        self.rb_pulse_pin = Pin(19, Pin.IN, Pin.PULL_UP)
        self.motor_rb = FIT0441(self.rb_direction_pin, self.rb_speed_pin, self.rb_pulse_pin)
        self.motor_rb.name = 'Right Back'

        self.left_motor_list = [self.motor_lb, self.motor_lf]
        self.right_motor_list = [self.motor_rb, self.motor_rf]
        self.all_motors_list = [self.motor_lb, self.motor_lf, self.motor_rb, self.motor_rf]
        super().__init__(self.left_motor_list, self.right_motor_list)
    
    def close(self):
        self.stop()
        self.lb_speed_pin.deinit()
        self.rb_speed_pin.deinit()
        self.lf_speed_pin.deinit()
        self.rf_speed_pin.deinit()
        

class Volts():

    def __init__(self, pin):
        self.pin = pin

    def read_volts(self):
        conversion_factor = 0.000545   #  10:1 voltage divider
        raw = self.pin.read_u16()
        volts = raw * conversion_factor
        return volts
        

class Buzzer():     # Buzzer Pin is declared, e.g.: PWM(Pin(19))
    def __init__(self, pin):
        self.pin = pin
        self.octaves = []    #  Octaves starting at C.  12 tone scales
        self.octaves.append([262,277,294,311,330,349,370,392,415,440,466,494])  #     C, C#, D, D#, E, F, F#, G, G#, A, B♭, B

    def play_note(self, octave, note, milliseconds):
        octave_index = octave - 1
        if octave_index > len (self.octaves) - 1:
            octave_index = 0
        if octave_index < 0:
            octave_index = 0

        note_index = note - 1
        if note_index > len (self.octaves[octave_index]) - 1:
            note_index = 0
        if note_index < 0:
            note_index = 0
        
        self.pin.duty_u16(1000)
        frequency = self.octaves[octave_index][note_index]
        print (frequency)
        self.pin.freq(frequency)
        utime.sleep_ms(milliseconds)
        self.pin.duty_u16(0)

    def play_beep(self):
        #print ("beep")
        self.play_note(1, 2, 600)

    def play_ringtone(self):
        song = []
        song.append([3,700])
        song.append([6,300])
        song.append([3,400])
        song.append([9,800])

        for note in song:
            self.play_note(1, note[0], note[1])

class Headlights():
    
    def __init__(self, led_pins, leds_on):
        self.led_pins = led_pins     # This is an array of Pin objects with LEDs attached
        self.leds_on = leds_on       # This is an array of directions, e.g. ["fwd","spin_left"]

    def lights_switch(self, direction):
        if ((len(self.led_pins) > 0) and (direction in self.leds_on)):
            self.lights_on(direction)
        else:
            self.lights_off()

    def lights_on(self, direction):
        for led in self.led_pins:
            led.on()
        
    def lights_off(self):
        for led in self.led_pins:
            led.off()
        

class BrushedMotorPair():
    
    def __init__(self, board, left_motor, right_motor, lights=None):
        self.board = board
        self.left = left_motor
        self.right = right_motor
        self.lights = lights
        self.last_spin = ""
        self.left_fwd = "r"
        self.right_fwd = "f"
        self.left_rev = "f"
        self.right_rev = "r"

    def do_lights(self, direction):
        if self.lights != None:
            self.lights.lights_switch(direction)

    def convert_millimetres_to_milliseconds(self, millimetres, speed):
        milliseconds = int (float(millimetres * 220) / math.pow(speed,0.5))
        return milliseconds

    def convert_degrees_to_milliseconds(self, millimetres, speed):
        degrees = int (float(millimetres * 210) / math.pow(speed,0.5))
        return degrees

    def fwd(self, millimetres, speed):
        self.do_lights("fwd")
        self.board.motorOn(self.right, self.right_fwd, speed)
        self.board.motorOn(self.left, self.left_fwd, speed)
        utime.sleep_ms(self.convert_millimetres_to_milliseconds(millimetres, speed))
        self.board.motorOff(self.right)
        self.board.motorOff(self.left)
        self.do_lights("")

    def rev(self, millimetres, speed):
        self.do_lights("rev")
        self.board.motorOn(self.right, self.right_rev, speed)
        self.board.motorOn(self.left, self.left_rev, speed)
        utime.sleep_ms(self.convert_millimetres_to_milliseconds(millimetres, speed))
        self.board.motorOff(self.right)
        self.board.motorOff(self.left)
        self.do_lights("")

    def spin_left(self, degrees, speed):
        self.do_lights("spl")
        self.board.motorOn(self.right, self.right_fwd, speed)
        self.board.motorOn(self.left, self.left_rev, speed)
        utime.sleep_ms(self.convert_degrees_to_milliseconds(degrees, speed))
        self.board.motorOff(self.right)
        self.board.motorOff(self.left)
        self.last_spin = "L"
        self.do_lights("")

    def spin_right(self, degrees, speed):
        self.do_lights("spr")
        self.board.motorOn(self.right, self.right_rev, speed)
        self.board.motorOn(self.left, self.left_fwd, speed)
        utime.sleep_ms(self.convert_degrees_to_milliseconds(degrees, speed))
        self.board.motorOff(self.right)
        self.board.motorOff(self.left)
        self.last_spin = "R"
        self.do_lights("")

    def stop(self):
        self.board.motorOff(self.right)
        self.board.motorOff(self.left)
        self.do_lights("")

class HCSR04():

    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.error_code = 0
        self.error_message = ""
        
    def millimetres(self):
        start_ultra = utime.ticks_us()
        self.trigger.low()
        utime.sleep_ms(10)
        self.trigger.high()
        utime.sleep_us(10)
        self.trigger.low()
        success = False
        for i in range(20000):
            if self.echo.value() == 1:
                signaloff = utime.ticks_us()
                success = True
                break
        if not success:
            duration1 = (utime.ticks_us() - start_ultra) / 1000
            self.error_code = 1
            self.error_message = "Failed 1 after " + str(duration1) + " milliseconds"
            return 0
        success = False
        for i in range(10000):
            if self.echo.value() == 0:
                signalon = utime.ticks_us()
                success = True
                break
        if not success:
            duration2 = (utime.ticks_us() - signaloff) / 1000
            self.error_code = 2
            self.error_message = "Failed 2 after " + str(duration2) + " milliseconds"
            return 0
        timepassed = signalon - signaloff
        distance = (timepassed * 0.343) / 2
        self.last_distance_measured = distance
        return distance

if __name__ == "__main__":
    print ('col_objects_v11.py')
