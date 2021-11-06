import this_robot_v07 as this_robot
import collections
utime = this_robot.utime

def execute_command_stack(command_stack):
    while True:
        try:
            command_tuple = command_stack.popleft()
            print (command_tuple)
            my_drive_train.drive(command_tuple)
            utime.sleep_ms(command_tuple[3])
        except IndexError:
            print ("No more commands")
            break

print ("")
print ("Starting motor test")

me = this_robot.ThisRobot()
my_drive_train = me.drive_train

max_queue_length = 9

commands = {}

command_name = 'JUST_STOP'
commands[command_name] = {}
commands[command_name]['COMMANDS'] = [(0,0,10,10)]   #  tuple is: left %, right %, run up time, steady time
commands[command_name]['INITIATING_BUTTON'] = ''
commands[command_name]['NAME'] = 'Just Stop'

command_name = 'LOOP_ROUND'
commands[command_name] = {}
commands[command_name]['COMMANDS'] = [(50,50,400,1000),(25,75,500,1000),(50,50,500,1000),(0,0,100,10)]
commands[command_name]['INITIATING_BUTTON'] = ''
commands[command_name]['NAME'] = 'Loop Round'

command_name = 'FWD_AND_REV'
commands[command_name] = {}
commands[command_name]['COMMANDS'] = [(50,50,500,1000),(-50,-50,500,1000),(0,0,500,10)]
commands[command_name]['INITIATING_BUTTON'] = ''
commands[command_name]['NAME'] = 'Forwards and Reverse'

command_name = 'GO_AND_STOP'
commands[command_name] = {}
commands[command_name]['COMMANDS'] = [(50,50,1000,1000),(0,0,1000,10)]
commands[command_name]['INITIATING_BUTTON'] = ''
commands[command_name]['NAME'] = 'Go and Stop'

# NOTE: Blue button is hard-wired reset
commands['LOOP_ROUND']['INITIATING_BUTTON'] = 'YELLOW_BUTTON'
commands['FWD_AND_REV']['INITIATING_BUTTON'] = 'GREEN_BUTTON'

while True:
    for command in commands:
        this_command = commands[command]
        button = this_command['INITIATING_BUTTON']
        if button:
            button_pressed = not me.inputs[button]['PIN'].value()
            if button_pressed:
                print (' ')
                print (this_command['NAME'])
                command_list = this_command['COMMANDS']
                my_queue = collections.deque((),max_queue_length)
                for i in range(len(command_list)):
                    my_queue.append(command_list[i])
                execute_command_stack(my_queue)
    utime.sleep_ms(25)

for motor in my_drive_train.all_motors:
    motor.duty_u16(0)

print ("")
print ("Starting motor test")
print ("")
