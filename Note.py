import typing

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Note:

	names = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b']

	def __init__ (self, pitch, velocity, delta_time):	# as midi note
		self.pitch = pitch
		self.velocity = velocity
		self.duration = delta_time

	def __str__ (self) -> str:									# as humdrum token
		m = ((self.pitch-60) % 12)	# pitch class
		n = Note.names[m] # pitch name
		n = n if self.pitch >= 60 else n.capitalize() # capitalize if below middle C
		o = abs(int((self.pitch/12)-5)) # calculate octave (0 is the octave of middle C)
		while o:
			n = n[0] + n # mark octave using humdrum note name repetition.
			o -= 1
		return '4' + str(n)