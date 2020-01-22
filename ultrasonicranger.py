import utime
from microbit import sleep, pin0
class UltrasonicRanger:
    def __init__(self,pin=pin0):
        self.pin=pin
    def get(self):
        self.pin.write_digital(0)
        sleep(2)
        self.pin.write_digital(1)
        sleep(10)
        self.pin.write_digital(0)
        timeout = utime.ticks_us()+3000
        while not self.pin.read_digital():
            if timeout < utime.ticks_us():
                return 0
        ts = utime.ticks_us()
        while self.pin.read_digital():
            pass
        return (utime.ticks_us()-ts)/28/2
