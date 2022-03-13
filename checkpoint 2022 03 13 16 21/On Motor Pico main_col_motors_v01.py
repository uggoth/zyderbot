import machine
import utime
import col_objects_motor_v19 as colobj

progname = 'main_col_motors_v01.py'

my_stream = colobj.CommandStream()

if not my_stream.valid:
    print ('**** Failed to open stream')

led_onboard=machine.Pin(25, machine.Pin.OUT)

start_button = colobj.ThisStartButton()
rgb_led = start_button.rgb_led
this_drive_train = colobj.ThisDriveTrain()
this_drive_train.stop()

while True:
    message = my_stream.get(1)
    if not message:
        continue
    else:
        command = message[0:4]
        if command == 'WHOU':
            my_stream.send(colobj.who_me)
        elif command == 'SOFT':
            my_stream.send(progname)
        elif command == 'BLON':
            my_stream.send('OKOK')
            led_onboard.on()
        elif command == 'BLOF':
            my_stream.send('OKOK')
            led_onboard.off()
        elif command == 'BLU+':
            my_stream.send('OKOK')
            rgb_led.blue.on()
        elif command == 'BLU-':
            my_stream.send('OKOK')
            rgb_led.blue.off()
        elif command == 'GRE+':
            my_stream.send('OKOK')
            rgb_led.green.on()
        elif command == 'GRE-':
            my_stream.send('OKOK')
            rgb_led.green.off()
        elif command == 'RED+':
            my_stream.send('OKOK')
            rgb_led.red.on()
        elif command == 'RED-':
            my_stream.send('OKOK')
            rgb_led.red.off()
        elif command == 'ECHO':
            my_stream.send ('ECHO:' + command)
        elif command == 'EXIT':
            my_stream.send ('Exiting')
            break
        elif command == 'STOP':
            my_stream.send('OKOK')
            rgb_led.green.off()
            this_drive_train.stop()
        elif command == 'DRIV':
            angle = int(message[4:8])
            speed = int(message[8:12])
            smoothness = int(message[12:16])
            my_stream.send('OKOK')
            rgb_led.green.on()
            this_drive_train.drive(angle, speed, smoothness)           
        else:
            my_stream.send ('**** did not understand ' + command)

my_stream.close()
