from microbit import pin0

class VibrationMotor:
	def __init__(self,pin=pin0):
		self.pin=pin
	def on(self):
		self.pin.write_digital(1)
	def off(self):
		self.pin.write_digital(0)
