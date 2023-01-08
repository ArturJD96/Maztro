import requests
import time

import Sequence

class Listener:

	def __init__ (self, progression, sequencer, debug=False, offline=False):
		print(type(progression))
		print(type(sequencer))
		self.progression = progression
		self.sequence = sequence

		self._debug = debug
		self._offline = offline

	def __call__ (self, event:tuple, data=None) -> None:	# ...

		midi_message, delta_time = event

		msb = None
		pitch = None
		vel = None

		# manage recording:
		condition = None # use pads of MPK or start/resume and stop button.
		is_note = len(midi_message) == 3
		if is_note:
			msb, pitch, vel = midi_message
			msb_note_on  = 0x99
			#msb_note_off = 0x89
			key_recording = 4
			if (msb == msb_note_on) and (pitch == key_recording) and (vel > 0):
				self.sequence.toggle()
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
		else:
			msb = midi_message[0]
			if msb == 250 or msb == 251: #midi play or resume
				self.sequence.records = True
				print('RECORDING ON')
				self.progression = Progression()
				self.time = 0
			elif msb == 252: #midi stop
				print(f'RECORDING OFF\n{self.progression}')
				print('KERN TO BE DISPLAYED AS INPUT:\n' + self.progression.get_display())
				if not self._offline:
					requests.post('http://127.0.0.1:5000', data = {"inputkern": str(self.progression)})
				correlations = Correlations_in_kern_repository(str(self.progression))
							
		# what could be recorded:
		if self.sequence.records and (msb == 0x90 or msb == 0x80):
			self.time += delta_time
			self.progression += Note(pitch, vel, self.time, delta_time)
			# print(pitch, vel, self.time, delta_time)	# my fail: passed by value or reference?
			# tag = f'<script>{self.progression}</script>'

	def enter_listener_loop (self):
		flag = True
		while True:
			if self._debug and flag:
				print('~ ~ ~ mock midi ~ ~ ~')
				messages = [
					[250],
					[0x99,80,127],
					[0x89,80,0],
					[0x99,78,127],
					[0x89,78,0],
					[0x99,72,127],
					[0x89,72,0],
					[252]
				]
				for message in messages:
					# mocking midi callback
					self.handle_incoming_midi((message, 0))
					time.sleep(0.1)
				print('~ ~ ~ all messages sent ~ ~ ~')
				flag = False
			else:
				print('dupa')
				time.sleep(0.05)