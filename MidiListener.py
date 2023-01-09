import requests
import time

from Note import Note
from Progression import Progression
from Correlations import Correlations_in_kern_repository

class MidiListener:

	def __init__ (self, sequence, debug=False, offline=False):

		self.progression:'Progression' = None
		self.sequence:'Sequence' = sequence

		self._debug = debug
		self._offline = offline
		self._active = True

	def __call__ (self, event:tuple, data=None) -> None:	# ...
		
		# Define data
		midi, delta_time = event
		msb,pitch,vel = midi if len(midi) == 3 else (midi[0], None, None)

		# Actions for msb values triggering recording the sequence
		if msb in [250,251,252,0x99]:

			# Type
			if (msb == 0x99) and (pitch == 4) and (vel > 0):
				self.sequence.toggle()
			else:
				self.sequence.records = not (msb == 252)

			# Recording On (or Off)
			if self.sequence.records:
				print('RECORDING ON')
				self.progression = Progression()
				self.sequence.time = 0
			else:
				print(f'RECORDING OFF\n{self.progression}')
				print('KERN TO BE DISPLAYED AS INPUT:\n' + self.progression.get_display())
				if not self._offline:
					requests.post('http://127.0.0.1:5000', data = {"inputkern": str(self.progression)})
				correlations = Correlations_in_kern_repository(str(self.progression))

		elif self.sequence.records and (msb == 0x90 or msb == 0x80):
			self.sequence.time += delta_time
			self.progression += Note(pitch, vel, self.sequence.time, delta_time)
			# print(pitch, vel, self.time, delta_time)	# my fail: passed by value or reference?
			# tag = f'<script>{self.progression}</script>'

	@staticmethod
	def activate (listener:'MidiListener', debug=False):
		if debug:
			MidiListener.mock(listener)
		else:
			print('~ ~ ~ ... listening ... ~ ~ ~')
			while listener._active:
				time.sleep(0.05)	# reduce resolution to save CPU.

	@staticmethod
	def mock (listener:'MidiListener'):
		print('~ ~ ~ send mock midi messages ~ ~ ~')
		messages = [
			[250],
			[0x90,80,127],
			[0x80,80,0],
			[0x90,78,127],
			[0x80,78,0],
			[0x90,72,127],
			[0x80,72,0],
			[252]
		]
		for message in messages:
			# mocking midi callback
			listener((message, 0))
			time.sleep(0.1)
		print('~ ~ ~ all mock midi messages sent ~ ~ ~')