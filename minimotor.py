from microbit import i2c

# I2C Mini Motor Driver
MOTORA_DRV8830 = (0x62)
MOTORB_DRV8830 = (0x60)

class MiniMotor():
    def __init__(self, motorNumber=0):
        self.motorAddress = MOTORA_DRV8830
        if (motorNumber == 1):
            self.motorAddress = MOTORB_DRV8830
    def getAddress(self):
        return self.motorAddress
    def getFault(self):
        i2c.write(self.motorAddress, b'\x01')
        return i2c.read(self.motorAddress, 8);
    def clearFault(self):
        i2c.write(self.motorAddress, bytearray([1, 128]))
    def drive(self, speed):
        # first clear any fault
        self.clearFault()
        buf = abs(speed)
        if (buf > 63):
            buf = 63
            buf = buf << 2
        if (speed < 0):
            buf |= 0x01
        else:
            buf |= 0x02
        i2c.write(self.motorAddress, bytearray([0, buf]))
    def stop(self):
        i2c.write(self.motorAddress, bytearray([0, 0]))
    def brake(self):
        i2c.write(self.motorAddress, bytearray([0, 3]))
