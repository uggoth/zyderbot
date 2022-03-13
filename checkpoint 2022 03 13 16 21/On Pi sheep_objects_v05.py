import smbus
import pigpio
import serial
import time
import sys, select

def get_pico(code):
    pico = Pico(code)
    if not pico.valid:
        return False
    else:
        return pico

class Pico():

    def __init__(self, pico_id):

        self.possible_picos = {'SHEEP':'Sheep Pico',
                               'HORSE':'Dummy Test Pico',
                               'MOTOR':'Motor Pico'}
        self.possible_ports = ['/dev/ttyACM0',
                               '/dev/ttyACM1',
                               '/dev/ttyACM2',
                               '/dev/ttyACM3']
        self.port_name = 'Unknown'
        self.id = 'Unknown'
        self.name = 'Unknown'
        self.port = None
        self.valid = False

        if pico_id not in self.possible_picos:
            #print ('**** ',pico_id,'not known')
            return
        
        for possible_port in self.possible_ports:
            time.sleep(0.01)
            try:
                test_port = serial.Serial(possible_port,
                                          timeout=0.1,
                                          write_timeout=0.1,
                                          baudrate=115200)
            except:
                #print (possible_port,'failed to open')
                continue
            self.port = test_port
            if not self.send('WHOU'):
                #print ('**** send failed')
                self.port.close
                continue
            result = self.get()
            if not result:
                #print ('**** get failed')
                self.port.close
                continue
            if result == pico_id:
                self.name = self.possible_picos[pico_id]
                self.id = pico_id
                self.port_name = possible_port
                self.valid = True
                return
            else:
                self.port.close
                continue

    def __str__(self):
        return self.name

    def send(self, text):
        in_text = text + '\n'
        out_text = in_text.encode('utf-8')
        try:
            self.port.write(out_text)
        except:
            print ('write failed')
            return False
        return True

    def get(self, timeout=0.01):
        inputs, outputs, errors = select.select([self.port],[],[],timeout)
        if len(inputs) > 0:
            read_text = self.port.readline()
            decoded_text = read_text.decode('utf-8')[:-2]
            return decoded_text
        else:
            return False

    def flush(self):
        more = 1
        timeout=0.001
        flushed = 0
        while more > 0:
            inputs, outputs, errors = select.select([self.port],[],[],timeout)
            more = len(inputs)
            if more > 0:
                discard = self.port.readline()
                flushed += 1
        return flushed

    def close(self):
        self.port.close()

class gpio_listener():

    def __init__(self, this_gpio, pin_no, name, pullup=True):
        self.this_gpio = this_gpio
        self.pin_no = pin_no
        self.name = name
        this_gpio.set_mode(pin_no, pigpio.INPUT)
        if pullup:
            this_gpio.set_pull_up_down(pin_no, pigpio.PUD_UP)

    def get(self):
        return self.this_gpio.read(self.pin_no)

    def __str__(self):
        return "{} {}".format(self.name,self.get())

    def set_callback(self, callback):
        self.callback_handle = self.this_gpio.callback(self.pin_no, pigpio.EITHER_EDGE, callback)

    def unset_callback(self):
        self.callback_handle.cancel()

class feedback():

    def __init__(self):
        self.my_gpio = pigpio.pi()
        self.moving = 1

if __name__ == "__main__":
    print ('pico_utils_v03.py')
