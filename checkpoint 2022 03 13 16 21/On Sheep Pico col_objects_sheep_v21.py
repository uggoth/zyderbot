#  Useful Objects from Colin Walls

from machine import Pin, PWM
import utime
import math
import sys, select

who_me = 'SHEEP'

class CommandStream():
    
    in_use = False
    
    def __init__(self):
        if CommandStream.in_use:
            self.valid = False
        else:
            CommandStream.in_use = True
            self.valid = True
    
    def close(self):
        CommandStream.in_use = False

    def get(self, delay=0.001):
        inputs, outputs, errors = select.select([sys.stdin],[],[],delay)
        if (len(inputs) > 0):
            result = sys.stdin.readline()
        else:
            result = False
        return result
 
    def send(self, message):
        print (message)
 
    def flush(self):
        no_inputs = 1
        while no_inputs > 0:
            inputs, outputs, errors = select.select([sys.stdin],[],[],0.001)
            if (len(inputs) > 0):
                result = sys.stdin.readline()
            else:
                break

class Servo():
    
    def __init__(self, board, port):
        self.port = port
        self.board = board
        self.min_angle = 0
        self.max_angle = 180
        #  NOTE: positions must be overriden. This is just reserving memory
        self.positions = {'PARK':0,'PREP':0,'PREVIOUS':0,'INCREMENT':0,'TARGET':0,'HERD':0,'WIDE':0,'GRAB':0}
    
    def move_to(self, degrees):
        int_degrees = int(degrees)
        if int_degrees < self.min_angle:
            my_degrees = self.min_angle
            result = False
        elif int_degrees > self.max_angle:
            my_degrees = self.max_angle
            result = False
        else:
            my_degrees = int_degrees
            result = True
        self.board.servoWrite(self.port, my_degrees)
        self.previous_degrees = my_degrees
        return result

    def position(self, code):
        if code in self.positions:
            return self.move_to(self.positions[code])
        else:
            print ('**** unknown position', code)
            return False
        
    def park(self):
        return self.position('PARK')
    
    def grab(self):
        return self.position('GRAB')
    
    def wide(self):
        return self.position('WIDE')

    def prep(self):
        return self.position('PREP')

    def herd(self):
        return self.position('HERD')

class LeftShoulder(Servo):
    def __init__(self, board):
        super().__init__(board, 1)
        self.name = 'Left Shoulder'
        self.min_angle = 10
        self.max_angle = 125
        self.positions['PARK'] = 10
        self.positions['PREP'] = 110
        self.positions['WIDE'] = 100
        self.positions['GRAB'] = 125
        self.positions['HERD'] = 125
        self.positions['PREVIOUS'] = self.positions['PARK']  #  starting position ASSUMED

class LeftElbow(Servo):
    def __init__(self, board):
        super().__init__(board, 2)
        self.name = 'Left Elbow'
        self.min_angle = 0
        self.max_angle = 170
        self.positions['PARK'] = 105
        self.positions['PREP'] = 105
        self.positions['WIDE'] = 160
        self.positions['GRAB'] = 125
        self.positions['HERD'] = 125
        self.positions['PREVIOUS'] = self.positions['PARK']  #  starting position ASSUMED

class RightShoulder(Servo):
    def __init__(self, board):
        super().__init__(board, 3)
        self.name = 'Right Shoulder'
        self.min_angle = 10
        self.max_angle = 125
        self.positions['PARK'] = 125
        self.positions['PREP'] = 25
        self.positions['WIDE'] = 15
        self.positions['GRAB'] = 55
        self.positions['HERD'] = 55
        self.positions['PREVIOUS'] = self.positions['PARK']  #  starting position ASSUMED
    
class RightElbow(Servo):
    def __init__(self, board):
        super().__init__(board, 4)
        self.name = 'Right Elbow'
        self.min_angle = 0
        self.max_angle = 180
        self.positions['PARK'] = 95
        self.positions['PREP'] = 95
        self.positions['WIDE'] = 25
        self.positions['GRAB'] = 110
        self.positions['HERD'] = 110
        self.positions['PREVIOUS'] = self.positions['PARK']  #  starting position ASSUMED

class Attachment():

    def __init__(self, board):
        self.left_shoulder = LeftShoulder(board)
        self.left_elbow = LeftElbow(board)
        self.right_shoulder = RightShoulder(board)
        self.right_elbow = RightElbow(board)
        self.servos = {'LEFT_SHOULDER':self.left_shoulder,
                       'RIGHT_SHOULDER':self.right_shoulder,
                       'LEFT_ELBOW':self.left_elbow,
                       'RIGHT_ELBOW':self.right_elbow}
        self.attachment_code = 'SHEEP'
        self.valid = True
        self.poses = {'PARK_ALL':{'LEFT_SHOULDER':'PARK','LEFT_ELBOW':'PARK','RIGHT_SHOULDER':'PARK','RIGHT_ELBOW':'PARK'},
                      'PARK_LEFT':{'LEFT_SHOULDER':'PARK','LEFT_ELBOW':'PARK'},
                      'PARK_RIGHT':{'RIGHT_SHOULDER':'PARK','RIGHT_ELBOW':'PARK'},
                      'PREP_RIGHT':{'RIGHT_SHOULDER':'PREP','RIGHT_ELBOW':'PREP'},
                      'PREP_LEFT':{'LEFT_SHOULDER':'PREP','LEFT_ELBOW':'PREP'},
                      'GRAB':{'LEFT_SHOULDER':'GRAB','LEFT_ELBOW':'GRAB','RIGHT_SHOULDER':'GRAB','RIGHT_ELBOW':'GRAB'},
                      'HERD':{'LEFT_SHOULDER':'HERD','LEFT_ELBOW':'HERD','RIGHT_SHOULDER':'HERD','RIGHT_ELBOW':'HERD'},
                      'WIDE_RIGHT':{'RIGHT_SHOULDER':'WIDE','RIGHT_ELBOW':'WIDE'},
                      'WIDE_LEFT':{'LEFT_SHOULDER':'WIDE','LEFT_ELBOW':'WIDE'},
                      'WIDE':{'LEFT_SHOULDER':'WIDE','LEFT_ELBOW':'WIDE','RIGHT_SHOULDER':'WIDE','RIGHT_ELBOW':'WIDE'}
                      }

    def do_pose(self, pose_code, smoothness=0):  #  NOTE smoothness is in milliseconds
        if pose_code not in self.poses:
            return False
        #print ('doing pose', pose_code)
        for servo_code in self.poses[pose_code]:
            servo = self.servos[servo_code]
            target_code = self.poses[pose_code][servo_code]
            target_position = servo.positions[target_code]
            servo.positions['TARGET'] = target_position
            #print (servo_code, target_code, target_position)
        if smoothness > 5:
            if smoothness < 100:
                loops = int(smoothness)
                interval = 1
            else:
                loops = 100
                interval = int(float(smoothness) / 100.0)
            for i in range(loops):
                utime.sleep_ms(interval)
                for servo_code in self.poses[pose_code]:
                    servo = self.servos[servo_code]
                    old_pos = servo.positions['PREVIOUS']
                    new_pos = servo.positions['TARGET']
                    diff = new_pos - old_pos
                    increment = int(float(diff) / float(loops) * float(i))
                    mid_pos = old_pos + increment
                    servo.move_to(mid_pos)
        for servo_code in self.poses[pose_code]:
            servo = self.servos[servo_code]
            target = servo.positions['TARGET']
            servo.move_to(target)
            servo.positions['PREVIOUS'] = target
        #print ('finished pose', pose_code)
        return True

    def close(self):
        pass

class RGBLED():
    def __init__(self):
        self.red = Pin(5, Pin.OUT)
        self.green = Pin(6, Pin.OUT)
        self.blue = Pin(7, Pin.OUT)
    def off(self):
        self.red.off()
        self.green.off()
        self.blue.off()

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
    print ('col_objects_sheep_v20.py')
