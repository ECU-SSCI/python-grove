from microbit import sleep, pin0
class Servo:
	def __init__(self,pin=pin0):
		self.pin=pin
	def set(self, val):
		self.pin.write_analog(val)
