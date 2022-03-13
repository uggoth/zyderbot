import serial
import time
import json
import sys
import sheep_objects_v05 as sheepobj

def drive(angle, speed, smoothness, delay):
    global motor_pico
    my_angle = angle % 360
    my_speed = speed % 100
    my_smoothness = smoothness % 10000
    command_line = '{:}{:04}{:04}{:04}'.format('DRIV',my_angle,my_speed,my_smoothness)
    motor_pico.send(command_line)
    print(command_line,'receives',motor_pico.get())
    time.sleep(delay)

def stop(delay):
    global motor_pico
    command = 'STOP'
    motor_pico.send(command)
    reply = motor_pico.get()
    print (command,'receives',reply)
    time.sleep(delay)    

last_id = 0

def pose(pose_code, smoothness, delay):
    global last_id, sheep_pico
    last_id += 1
    command = json.dumps({'POSE':pose_code,'SMOOTHNESS':smoothness, 'ID':last_id})
    sheep_pico.send(command)
    reply = sheep_pico.get()
    print (command,'receives',reply)
    time.sleep(delay)    
    
sheep_pico = sheepobj.get_pico('SHEEP')
if not sheep_pico:
    print ('failed to get sheep')
    sys.exit(1)

motor_pico = sheepobj.get_pico('MOTOR')
if not motor_pico:
    print ('failed to get motor')
    sys.exit(1)

pose('PREP_RIGHT',1000,1)
pose('PREP_LEFT',1000,1)
drive(angle=0,speed=45,smoothness=400,delay=1)
stop(1)
pose('GRAB',1000,1)
drive(angle=180,speed=45,smoothness=400,delay=0.5)
stop(1)
pose('WIDE',2000,4)
drive(angle=180,speed=45,smoothness=400,delay=0.5)
stop(1)
pose('PARK_LEFT',2000,4)
pose('PARK_RIGHT',2000,4)

motor_pico.close()
sheep_pico.close()
