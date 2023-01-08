import typing
import warnings
import sys
import time
import asyncio
import rtmidi
import requests

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note
from Sequence import Sequence
from Progression import Progression
from MidiListener import Listener
from Utilities import Hardware_Warning
from Correlations import Correlations_in_kern_repository

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MainApp:

	default_keyboard_name = 'MPK mini 3'

	def __init__ (self, keyboard_name:str=None, debug:bool=False, offline:bool=False):
		self.keyboard_name = keyboard_name if keyboard_name is not None else MainApp.default_keyboard_name
		self.midiin = rtmidi.MidiIn()
		self.is_recording = False			#
		self.progression:Progression = None	#
		self.time:float = None		#

		self._debug:bool = debug # outputs mock midi input for testing purposes when keyboard no keyboard detected
		self._offline:bool = offline # turns off posting requests in handle_incoming_midi method (the midi listener func).

	@property
	def ports (self) -> list[str]:
		return self.midiin.get_ports()

	def __call__ (self):
		self.midiin.set_callback(self.handle_incoming_midi, self)
		try:
			port_id:int = self.ports.index(self.keyboard_name)
			self.midiin.open_port(port_id)
			self.enter_listener_loop() #

		except ValueError as ve:
			keyboard_name = MainApp.default_keyboard_name
			if ve.args[0] == f"'{keyboard_name}' is not in list":
				warnings.warn(
					f"{keyboard_name} is not connected. Use your computer keyboard as midi keyboard.",
					Hardware_Warning)
			# listen to the keyboard strokes !
			self.midiin.open_virtual_port(self.keyboard_name)
			self.enter_listener_loop() #

	def __enter__ (self):
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self.midiin.__exit__(*sys.exc_info())

	def handle_incoming_midi (self, event:tuple, data=None) -> None:	# ...

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
				self.is_recording = not self.is_recording # toggle
				if self.is_recording:
					print('RECORDING ON')
					self.progression = Progression()
					self.time = 0
				else:
					print(f'RECORDING OFF\n{self.progression}')
					print('KERN TO BE DISPLAYED AS INPUT:\n' + self.progression.get_display())
					if not self._offline:
						print('Sending request...')
						requests.post('http://127.0.0.1:5000', data = {"inputkern": str(self.progression)})
					correlations = Correlations_in_kern_repository(str(self.progression))
		else:
			msb = midi_message[0]
			if msb == 250 or msb == 251: #midi play or resume
				self.is_recording = True
				print('RECORDING ON')
				self.progression = Progression()
				self.time = 0
			elif msb == 252: #midi stop
				print(f'RECORDING OFF\n{self.progression}')
				print('KERN TO BE DISPLAYED AS INPUT:\n' + self.progression.get_display())
				if not self._offline:
					print('Sending request...')
					requests.post('http://127.0.0.1:5000', data = {"inputkern": str(self.progression)})
				correlations = Correlations_in_kern_repository(str(self.progression))
							
		# what could be recorded:
		if self.is_recording and (msb == 0x90 or msb == 0x80):
			self.time += delta_time
			self.progression += Note(pitch, vel, self.time, delta_time)
			# print(pitch, vel, self.time, delta_time)	# my fail: passed by value or reference?
			# tag = f'<script>{self.progression}</script>'

	def enter_listener_loop (self):
		self.time = 0
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