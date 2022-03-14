import PicoRobotics
import utime

board = PicoRobotics.KitronikPicoRobotics()

left_shoulder = 1
left_elbow = 2
right_shoulder = 3
right_elbow = 4

board.servoWrite(right_shoulder, 90)
utime.sleep(1)
board.servoWrite(right_shoulder, 15)
utime.sleep(1)
board.servoWrite(right_shoulder, 90)
utime.sleep(1)
board.servoWrite(right_shoulder, 125)
