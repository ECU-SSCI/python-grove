from microbit import pin0
class Sound:
	def __init__(self,pin=pin0):
		self.pin=pin
	def get(self):
		val = 0
		for i in range(0,32):
			val += self.pin.read_analog()
		val >>= 5
		return val