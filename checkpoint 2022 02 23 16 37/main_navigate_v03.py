import utime
import col_objects_v11 as colobj
from machine import Pin
from i2c_slave_v03 import i2c_slave

def front_callback(ir_sensor, value):
    global keep_going
    keep_going = False

my_drive_train = colobj.ThisDriveTrain()
my_drive_train.stop()

i2c_s = i2c_slave()

my_stream = colobj.CommandStream(i2c_s)
front_ir = colobj.FrontIRArriving(front_callback)
keep_going = True

red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)
blue_led = Pin(16, Pin.OUT)

red_led.off()
green_led.off()
blue_led.off()

while True:
    green_led.on()
    command_code, angle, speed, smoothness, pulses = my_stream.get()
    green_led.off()
    blue_led.on()
    if command_code == 'D':  #  Drive
        result = my_drive_train.drive(angle, speed)
        if not result:
            green_led.off()
            blue_led.off()
            red_led.on()
        utime.sleep(0.5)

    elif command_code == 'S':  #  Stop
        my_drive_train.stop()
        blue_led.off()
    elif command_code == 'F':  #  check Forward IR
        my_drive_train.drive(angle, speed)
        seconds = 9
        loops = seconds * 1000
        keep_going = True
        for i in range(loops):
            utime.sleep_ms(1)
            if not keep_going:
                break
        my_drive_train.stop()
        blue_led.off()
    green_led.on()

blue_led.off()
green_led.off()
red_led.on()

my_drive_train.stop()
my_drive_train.close()
my_stream.close()
