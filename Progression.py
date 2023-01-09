import typing
import os

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression:

	directory = 'progressions'
	default_name = 'progression'

	def __init__ (self):
		self.notes = [] # array of tuples
		self.mode = 'midi2kern'
		self.chord_mode = False
		self.name:str = self.make_name()
		print(os.listdir(Progression.directory))
		with open(self.name, 'a+') as prog:
			prog.write('**kern\n')

	def __str__ (self) -> str:
		match self.mode:
			case 'midi2humMidi':
				return self.midi2humMidi()
			case 'midi2kern':
				return self.midi2kern()

	def __iadd__ (self, note:'Note') -> 'Progression':
		self.notes.append(note)
		if note.velocity > 0:
			with open(self.name, 'a') as prog:
				prog.write(f'{note}\n')
		return self

	def close(self):
		with open(self.name, 'a') as prog:
			prog.write('*-')

	def make_name(self) -> str:
		#name = f'{Progression.directory}/{Progression.default_name}_'
		file_names = os.listdir(Progression.directory)
		index = 1
		for n in file_names:
			if n.startswith(Progression.default_name):
				i = int(n.split('.')[0].split('_')[-1])
				if index < i:
					index = i + 1
		return f'{Progression.directory}/{Progression.default_name}_{index}.krn'

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

	def get_display (self) -> str:
		s = '**kern\t**kern\n*clefF4\t*clefG2\n'
		for note in self.notes:
			s += f'{note}\t.' if note.pitch >= 60 else f'.\t{note}'
			s += '\n'
		return s
