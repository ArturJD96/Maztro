import typing
import os

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression:

	def __init__ (self):
		self.notes = [] # array of tuples
		self.mode = 'midi2kern'
		self.chord_mode = False
		self.display = ProgressionDisplay()

	def __str__ (self) -> str:
		if self.mode == 'midi2humMidi':
			return self.midi2humMidi()
		elif self.mode == 'midi2kern':
				return self.midi2kern()

	def __iadd__ (self, note:'Note') -> 'Progression':
		self.notes.append(note)
		if note.velocity > 0:
			self.display.append(note)
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

	def get_display (self) -> str:
		s = '**kern\t**kern\n*clefF4\t*clefG2\n'
		for note in self.notes:
			s += f'{note}\t.' if note.pitch >= 60 else f'.\t{note}'
			s += '\n'
		return s

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class ProgressionDisplay:

	directory = 'virtual/templates'
	default_name = 'progression'

	def __init__ (self):
		self.name:str = self.make_name()
		self.kern = '**kern\t**kern\n*clefF4\t*clefG2\n*-\t*-'

	def __str__ (self):
		return self.kern

	def make_name(self) -> str:
		# file_names = os.listdir(ProgressionDisplay.directory)
		# print(file_names)
		# index = 1
		# for n in file_names:
		# 	if n.startswith(ProgressionDisplay.default_name):
		# 		i = int(n.split('.')[0].split('_')[-1])
		# 		if index <= i:
		# 			index = i + 1
		# return f'{ProgressionDisplay.directory}/{ProgressionDisplay.default_name}_{index}.krn'
		return f'{ProgressionDisplay.directory}/input.krn'

	def append (self, note:'Note') -> None:
		i = self.kern.rfind('\n')
		line = f'{note}\t.' if note.pitch >= 60 else f'.\t{note}'
		self.kern = f'{self.kern[:i+1]}{line}{self.kern[i:]}'
		with open(self.name, 'w') as file:
			file.write(self.kern)

	@staticmethod
	def reset_directory ():
		pass