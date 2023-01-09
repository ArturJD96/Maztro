import typing

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Note:

	names = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b']

	def __init__ (self, pitch:int, velocity:int, start_time:float, delta_time:float):	# as midi note
		self.pitch = pitch
		self.velocity = velocity
		self.start = start_time
		self.duration = delta_time

	def __str__ (self) -> str:		# as humdrum token

		m:int = (self.pitch-60) % 12	# pitch class
		n:str = Note.names[m] 			# pitch name

		if self.pitch < 60:
			n = n.capitalize()

		o = int(self.pitch/12) # calculate octave (5 is the octave of middle C)
		if o < 5:
			o *= -1
			o += 4
		else:
			o -= 5

		while o:
			n = n[0] + n # mark octave using humdrum note name repetition.
			o -= 1

		return n