import col_objects_sheep_v21 as colobj
import PicoRobotics

board = PicoRobotics.KitronikPicoRobotics()

sheep_attachment = colobj.Attachment(board)
if not sheep_attachment.valid:
    print ('**** Failed to open attachment')
    sys.exit(1)

re1 = colobj.RightElbow(board)
print (re1.name)

re2 = sheep_attachment.servos['RIGHT_ELBOW']
print (re2.name)


sheep_attachment.close()
