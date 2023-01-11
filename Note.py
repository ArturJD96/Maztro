# -*- coding: utf-8 -*-

import typing

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Note:

	names = ['c',['c#','d-'],'d',['d#','e-'],'e','f',['f#','g-'],'g',['g#','a-'],'a',['a#','b-'],'b']
	prev_note_name:str = ''
	prev_note_pc:int = 0
	prev_note_pitch:int = 0

	def __init__ (self, pitch:int, velocity:int, start_time:float, delta_time:float):	# as midi note
		self.pitch = pitch
		self.velocity = velocity
		self.start = start_time
		self.duration = delta_time

	def __str__ (self) -> str:		# as humdrum token

		pc:int = (self.pitch-60) % 12	# pitch class
		n = Note.names[pc] 				# pitch name (or list of names)

		# if isinstance(n, list):
		# 	n = n[0]

		# enharmony
		if len(n) > 1:
			d = self.pitch - Note.prev_note_pitch
			ns, nf = n
			if len(Note.prev_note_name) > 1 and len(n) > 1:	# previous and current note are chromatic
				if Note.prev_note_name[1] == '#':
					n = ns
				else:
					n = nf
			elif d == 0:
				n = Note.prev_note_name
			else:
				d_sign = d > 0
				d_odd = (d % 2) == 1
				if d_sign:
					if d_odd and d < 7:
						n = nf
					else:
						n = ns
				else:
					if d_odd and d < 7:
						n = ns
					else:
						n = nf

		Note.prev_note_pitch = self.pitch
		Note.prev_note_name = n

		if self.pitch < 60:
			n = n.capitalize()

		o = int(self.pitch/12) # calculate octave (5 is the octave of middle C)
		if o < 5:
			o *= -1
			o += 4
		else:
			o -= 5

		no = n[0]
		while o:
			no += no # mark octave using humdrum note name repetition.
			o -= 1
		
		if len(n) > 1:
			n = no + n[1]
		else:
			n = no

		print(n)

		return n