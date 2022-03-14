import col_objects_sheep_v21 as colobj
import PicoRobotics
import utime
import sys

def doit(pose, smoothness, delay):
    global sheep_attachment
    print ('pose',pose,'received',sheep_attachment.do_pose(pose, smoothness))
    utime.sleep_ms(delay)

board = PicoRobotics.KitronikPicoRobotics()

sheep_attachment = colobj.Attachment(board)
if not sheep_attachment.valid:
    print ('**** failed to open attachment')
    sys.exit(1)

doit('PARK_RIGHT',0, 200)
doit('PARK_LEFT',0, 200)
doit('PREP_RIGHT',1000, 2000)
doit('PREP_LEFT',1000, 2000)
doit('PARK_LEFT',1000, 200)
doit('PARK_RIGHT',1000, 2000)

sheep_attachment.close()
