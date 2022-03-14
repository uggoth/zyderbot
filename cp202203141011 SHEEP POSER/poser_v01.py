import sheep_objects_v05 as sheepobj
import sys
import time
import tkinter as tk
import json

def send_command(pico, command):
    pico.send(command)
    time.sleep(0.001)
    result = pico.get()  #  result
    return result

sheep_pico = sheepobj.get_pico('SHEEP')

if not sheep_pico:
    print ('** Failed to get sheep pico')
    sys.exit(1)
else:
    print ('Sheep pico found on ',sheep_pico.port_name)
    print (' ')

class Calibrator:
    def __init__(self, master, sheep_pico):
        self.master = master
        self.sheep_pico = sheep_pico
        self.frame_width = 700
        self.frame_height = 500
        self.frame = tk.Frame(master, width=self.frame_width, height=self.frame_height)
        self.frame.pack()

        self.right_shoulder_code = 'RIGHT_SHOULDER'
        self.right_shoulder_label = self.right_shoulder_code + '     <<<< OPEN'
        self.right_shoulder_park_value = 125
        self.right_shoulder_slider = tk.Scale(self.frame, command=self.right_shoulder_move,
                                        from_=0, to=180, resolution=5,
                                        length=650, sliderlength=20, 
                                        orient=tk.HORIZONTAL, label=self.right_shoulder_label)
        self.right_shoulder_slider.set(self.right_shoulder_park_value)
        self.right_shoulder_slider.place(x=20,y=20)

        self.right_elbow_code = 'RIGHT_ELBOW'
        self.right_elbow_label = self.right_elbow_code + '     <<<< OPEN'
        self.right_elbow_park_value = 95
        self.right_elbow_slider = tk.Scale(self.frame, command=self.right_elbow_move,
                                        from_=0, to=180, resolution=5,
                                        length=650, sliderlength=20, 
                                        orient=tk.HORIZONTAL, label=self.right_elbow_label)
        self.right_elbow_slider.set(self.right_elbow_park_value)
        self.right_elbow_slider.place(x=20,y=120)

        self.left_shoulder_code = 'LEFT_SHOULDER'
        self.left_shoulder_label = self.left_shoulder_code + '     <<<< CLOSE'
        self.left_shoulder_park_value = 10
        self.left_shoulder_slider = tk.Scale(self.frame, command=self.left_shoulder_move,
                                        from_=0, to=180, resolution=5,
                                        length=650, sliderlength=20, 
                                        orient=tk.HORIZONTAL, label=self.left_shoulder_label)
        self.left_shoulder_slider.set(self.left_shoulder_park_value)
        self.left_shoulder_slider.place(x=20,y=220)

        self.left_elbow_code = 'LEFT_ELBOW'
        self.left_elbow_label = self.left_elbow_code + '     <<<< CLOSE'
        self.left_elbow_park_value = 105
        self.left_elbow_slider = tk.Scale(self.frame, command=self.left_elbow_move,
                                        from_=0, to=180, resolution=5,
                                        length=650, sliderlength=20, 
                                        orient=tk.HORIZONTAL, label=self.left_elbow_label)
        self.left_elbow_slider.set(self.left_elbow_park_value)
        self.left_elbow_slider.place(x=20,y=320)

    def move_to(self, servo_code, where_to):
        command = json.dumps({'SERVO':servo_code,'MOVE_TO':where_to})
        sheep_pico.send(command)
        result = sheep_pico.get()
        if result != 'OKOK':
            print ('**** ERROR command ', command,'receives',result)

    def right_shoulder_move(self, where_to):
        self.move_to(self.right_shoulder_code, where_to)

    def right_elbow_move(self, where_to):
        self.move_to(self.right_elbow_code, where_to)

    def left_shoulder_move(self, where_to):
        self.move_to(self.left_shoulder_code, where_to)

    def left_elbow_move(self, where_to):
        self.move_to(self.left_elbow_code, where_to)

root = tk.Tk()
my_calibrator = Calibrator(root, sheep_pico)
root.mainloop()


time.sleep(1)
print ('closing')
sheep_pico.close()
time.sleep(1)
print ('finished')
