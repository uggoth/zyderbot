import col_objects_sheep_v21 as colobj
import PicoRobotics
import utime
import json
import sys

def doit(pose_code, smoothness, delay):
    result = sheep_attachment.do_pose(pose_code,smoothness)
    print ('pose',pose_code,'receives',result)
    print (' ')
    utime.sleep_ms(delay)

board = PicoRobotics.KitronikPicoRobotics()

sheep_attachment = colobj.Attachment(board)
if not sheep_attachment.valid:
    print ('**** Failed to open attachment')
    sys.exit(1)

led_onboard=machine.Pin(25, machine.Pin.OUT)

my_stream = colobj.CommandStream()
if not my_stream.valid:
    print ('**** Failed to open stream')
    sys.exit(1)

doit('PREP_RIGHT',500,1000)
doit('PREP_LEFT',500,1000)
doit('WIDE_RIGHT',500,4000)
doit('WIDE_LEFT',500,4000)
doit('PARK_LEFT',500,1000)
doit('PARK_RIGHT',500,1000)
