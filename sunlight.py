from microbit import i2c, sleep
from gc import collect

i2c.init()

class Sunlight():
	def __init__(self):
		while (self.read(0x00) != 0x45):
			print('Si1145 not ready...')
			sleep(1000)
		print('Si1145 preparing...')
		self.reset()
		self.deinit()
		print('Si1145 ready!')
	def read(self, reg, num_bytes=1, signed=False, le=False):
		i2c.write(0x60, bytearray([reg]))
		n = 0
		for x in reversed(i2c.read(0x60, num_bytes)):
			n <<= 8
			n |= x
		if signed:
			mask = 2**((num_bytes*8) - 1)
			n = -(n & mask) + (n & ~mask)
		collect()
		return n
	def reset(self):
		i2c.write(0x60, bytearray([0x08, 0x0]))
		i2c.write(0x60, bytearray([0x09, 0x0]))
		i2c.write(0x60, bytearray([0x04, 0x0]))
		i2c.write(0x60, bytearray([0x05, 0x0]))
		i2c.write(0x60, bytearray([0x06, 0x0]))
		i2c.write(0x60, bytearray([0x03, 0x0]))
		i2c.write(0x60, bytearray([0x21, 0xFF]))
		i2c.write(0x60, bytearray([0x18, 0x01]))
		sleep(100)
		i2c.write(0x60, bytearray([0x07, 0x17]))
		sleep(100)
	def deinit(self):
		i2c.write(0x60, bytearray([0X13, 0x29]))
		i2c.write(0x60, bytearray([0X14, 0x89]))
		i2c.write(0x60, bytearray([0X15, 0x02]))
		i2c.write(0x60, bytearray([0X16, 0x00]))
		print(self.writeParamData(0X01, 0x80|0x20|0x10|0x01) == 0x80|0x20|0x10|0x01)
		#set LED1 CURRENT(22.4mA)(It is a normal value for many LED)
		print(self.writeParamData(0X07, 0x03) == 0x03)
		i2c.write(0x60, bytearray([0X0F, 0X03]))
		print(self.writeParamData(0X02, 0x01) == 0x01)
		#PS ADC SETTING
		print(self.writeParamData(0X0B, 0X00) == 0x00)
		print(self.writeParamData(0X0A, 0X07) == 0x07)
		print(self.writeParamData(0X0C, 0X20|0X04) == 0X20|0X04)
		#VIS ADC SETTING
		print(self.writeParamData(0X11, 0X00) == 0x00)
		print(self.writeParamData(0X10, 0X07) == 0x07)
		print(self.writeParamData(0X12, 0X20) == 0x20)
		#IR ADC SETTING
		print(self.writeParamData(0X1E, 0X00) == 0x00)
		print(self.writeParamData(0X1D, 0X07) == 0x07)
		print(self.writeParamData(0X1F, 0X20) == 0x20)
		#interrupt enable
		i2c.write(0x60, bytearray([0X03, 0X01]))
		i2c.write(0x60, bytearray([0X04, 0x01]))  
		#AUTO RUN
		i2c.write(0x60, bytearray([0X08, 0xFF]))
		i2c.write(0x60, bytearray([0X18, 0X0F]))
	def readParamData(self, reg):
		i2c.write(0x60, bytearray([0x18, reg|0x80]))
		return self.read(0x2E)
	def writeParamData(self, reg, value):
		i2c.write(0x60, bytearray([0x17, value]))
		i2c.write(0x60, bytearray([0x18, reg|0xA0]))
		return self.read(0x2E)
	def getVisible(self):
		return self.read(0x22, 2)
	def getIR(self):
		return self.read(0x24, 2)
	def getProximity(PSn):
		return self.read(PSn, 2)
	def getUV(self):
		return self.read(0x2C, 2)/100.0