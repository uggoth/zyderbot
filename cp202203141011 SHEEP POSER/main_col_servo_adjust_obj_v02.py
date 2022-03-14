### adjust servo endpoints #########

import utime
import PicoRobotics
import col_objects_sheep_v21 as colobj

test_mode = True

board = PicoRobotics.KitronikPicoRobotics()

left_shoulder = colobj.LeftShoulder(board)
left_elbow = colobj.LeftElbow(board)
right_shoulder = colobj.RightShoulder(board)
right_elbow = colobj.RightElbow(board)

###### smaller numbers are clockwise
###### clockwise on right arm opens out
###### clockwise on left arm closes in

# right_shoulder: max clockwise is 10; max anticlockwise is 125
print (right_shoulder.move_to(25))
utime.sleep(1)

# right elbow : max clockwise is 0; max anticlockwise is 180; park is 95
print (right_elbow.move_to(25))
utime.sleep(2)

# left_shoulder: max clockwise is 10; max anticlockwise is 125
print (left_shoulder.move_to(95))
utime.sleep(1)

# left elbow : max clockwise is 0; max anticlockwise is 170; park is 95
print (left_elbow.move_to(170))
utime.sleep(2)

print (left_elbow.park())
utime.sleep(1)
print (left_shoulder.park())
utime.sleep(1)
print (right_elbow.park())
utime.sleep(1)
print (right_shoulder.park())
utime.sleep(1)
