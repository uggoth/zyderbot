import smbus
import pigpio

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

class command_stream():
    
    def split(self, num):
        num0 = num % 65536
        numb = num0 % 256
        numa = int((num0 - numb) / 256)
        return numa, numb
        
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def send(self, command_type, angle=0, speed=0, smoothness=0, pulses=0):
        command_code = ord(command_type)
        p1a, p1b = self.split(angle)
        p2a, p2b = self.split(speed)
        p3a, p3b = self.split(smoothness)
        p4a, p4b = self.split(pulses)
        command_array = [command_code, p1a, p1b, p2a, p2b, p3a, p3b, p4a, p4b]
        for byte in command_array:
            try:
                self.bus.write_byte(self.address,byte)
            except:
                print ('bad 1')
        return len(command_array)

    def get(self, no_bytes):
        result = 999
        try:
            result = self.bus.read_i2c_block_data(self.address, 1, no_bytes)
        except:
            print ('bad 2')
        return result

    def close(self):
        self.bus.close()

if __name__ == "__main__":
    print ('pico_utils_v02.py')
