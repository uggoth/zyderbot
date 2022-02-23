import sys
import time
import pico_utils_v02 as pico_utils
import smbus
import pigpio

def move(angle, speed, milliseconds):
    smoothness = 1
    my_stream.send('D', angle, speed, smoothness)
    time.sleep(milliseconds/1000.0)
    my_stream.send('S', 0, 0, 0)

program_name = sys.argv[0]
print (program_name,'Starting')

my_bus = smbus.SMBus(1)
i2c_address = 0x41

my_stream = pico_utils.command_stream(my_bus, i2c_address)

time.sleep(2)

move(angle=0, speed=25, milliseconds=1600)
move(angle=270, speed=25, milliseconds=725)
move(angle=0, speed=25, milliseconds=1600)
move(angle=270, speed=25, milliseconds=725)
move(angle=0, speed=25, milliseconds=1600)
move(angle=270, speed=25, milliseconds=725)
move(angle=0, speed=25, milliseconds=1600)
move(angle=270, speed=25, milliseconds=725)


my_stream.close()
print ('Finished')

