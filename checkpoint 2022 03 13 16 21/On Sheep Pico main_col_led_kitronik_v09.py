import machine
import utime
import col_objects_sheep_v21 as colobj
import PicoRobotics
import json
import sys

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

while True:
    message = my_stream.get(1)
    if not message:
        continue
    else:
        basic_commands = ['WHOU','SOFT','BLON','BLOF','ECHO','EXIT']
        command = message[0:4]
        if command in basic_commands:
            if command == 'WHOU':
                my_stream.send (colobj.who_me)
            elif command == 'SOFT':
                my_stream.send ('main_col_led_kitronik_v09.py')
            elif command == 'BLON':
                my_stream.send('OKOK')
                led_onboard.on()
            elif command == 'BLOF':
                my_stream.send('OKOK')
                led_onboard.off()
            elif command == 'ECHO':
                my_stream.send ('ECHO:' + command)
            elif command == 'EXIT':
                my_stream.send ('Exiting')
                break
        else:
            try:
                json_command = json.loads(message)
            except ValueError:
                my_stream.send ('**** Not valid JSON', message)
                continue

            if 'POSE' in json_command:
                pose = json_command['POSE']
            else:
                my_stream.send ('**** Cannot understand', message)
                continue
            
            if 'SMOOTHNESS' in json_command:
                smoothness = json_command['SMOOTHNESS']
            else:
                smoothness = 0
                
            if pose in sheep_attachment.poses:
                my_stream.send('OKOK')
                sheep_attachment.do_pose(pose, smoothness)
            else:
                my_stream.send ('**** Pose not known', message)

my_stream.close()
