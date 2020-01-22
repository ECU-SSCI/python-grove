from microbit import pin0, pin1
class Joystick:
	def __init__(self,x=pin0,y=pin1):
		self.x=x
		self.y=y
	def get_x(self):
		return self.x.read_analog()
	def get_y(self):
		return self.y.read_analog()
