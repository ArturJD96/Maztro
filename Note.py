# -*- coding: utf-8 -*-

import typing

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Note:

	names = ['c',['c#','d-'],'d',['d#','e-'],'e','f',['f#','g-'],'g',['g#','a-'],'a',['a#','b-'],'b']
	prev_note_name:str = ''
	prev_note_pc:int = 0

	def __init__ (self, pitch:int, velocity:int, start_time:float, delta_time:float):	# as midi note
		self.pitch = pitch
		self.velocity = velocity
		self.start = start_time
		self.duration = delta_time

	def __str__ (self) -> str:		# as humdrum token

		pc:int = (self.pitch-60) % 12	# pitch class
		n = Note.names[pc] 				# pitch name (or list of names)

		# enharmony
		if len(n) > 1:
			if pc > Note.prev_note_pc:
				n = n[1]
			elif pc == Note.prev_note_pc:
				n = Note.prev_note_n
			else:
				n = n[0]

		Note.prev_note_pc = pc
		Note.prev_note_name = n

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