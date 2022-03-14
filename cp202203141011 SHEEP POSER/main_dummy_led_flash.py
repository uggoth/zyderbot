import machine
import utime
led_onboard=machine.Pin(25, machine.Pin.OUT)
for i in range(10):
    led_onboard.on()
    utime.sleep(0.5)
    led_onboard.off()
    utime.sleep(0.2)
