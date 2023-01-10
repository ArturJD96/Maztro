import requests
import time
import typing

class MidiListener:

	def __init__ (self, synth:'fluidsynth', debug=False, offline=False):
		self.synth = synth

		self._debug = debug
		self._offline = offline
		self._active = True

	def __call__ (self, event:tuple, sequence:'Sequence') -> None:	# ...
		
		# Define variables
		midi, delta_time = event
		msb, pitch, vel = midi if (len(midi) == 3) else (midi[0], None, None)

		# Actions for msb values triggering recording the sequence
		if msb in [250,251,252,0x99]:
			# Start/Stop recording
			if (msb == 0x99) and (pitch == 4) and (vel > 0):
				sequence.records = not sequence.records
			else:
				sequence.records = not (msb == 252)

		elif sequence.records and (msb == 0x90 or msb == 0x80):
			self.synth.play_Note(pitch,0,vel)
			sequence.event(delta_time, event)

	@staticmethod
	def activate (listener:'MidiListener', debug=False):
		print('~ ~ ~ ... listening ... ~ ~ ~')
		while listener._active:
			time.sleep(0.05)	# reduce resolution to save CPU.

	@staticmethod
	def mock (listener:'MidiListener', sequence:'Sequence'):
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
			listener((message, 0), sequence)
			time.sleep(0.1)
		print('~ ~ ~ all mock midi messages sent ~ ~ ~')