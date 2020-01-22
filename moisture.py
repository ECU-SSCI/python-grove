from microbit import pin0
class Moisture:
	def __init__(self,pin=pin0):
		self.pin=pin
	def get(self):
		return 600/1024*self.pin.read_analog()
