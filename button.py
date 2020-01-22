from microbit import pin0
class Button:
	def __init__(self,pin=pin0):
		self.pin=pin
	def is_pressed(self):
		return pin.read_digital()
