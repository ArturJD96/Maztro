import typing

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression:

	def __init__ (self):
		self.notes = [] # array of tuples
		self.mode = 'midi2kern'
		self.chord_mode = False

	def __str__ (self) -> str:
		match self.mode:
			case 'midi2humMidi':
				return self.midi2humMidi()
			case 'midi2kern':
				return self.midi2kern()

	def __iadd__ (self, note:Note) -> 'Progression':
		self.notes.append(note)
		return self

	def midi2kern(self) -> str:
		if not self.chord_mode:
			return '**kern\n' + ''.join(f'{note}\n' for note in self.notes if note.velocity > 0)
		else:
			pass

	def midi2humMidi(self) -> str:
		if self.chord_mode:
			spines = []
			for i, note in enumerate(self.notes):
				pass
		else:
			return '**midi\n' + ''.join(f'{n.pitch}\n' for n in self.notes if n.velocity > 0) + '*-'
