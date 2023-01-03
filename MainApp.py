import typing
import warnings
import sys
import time
import asyncio
import rtmidi
from Correlations import Correlations_in_kern_repository

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note
from Progression import Progression
from Utilities import Hardware_Warning

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MainApp:

	default_keyboard_name = 'MPK mini 3'

	def __init__ (self, keyboard_name:str=None):
		self.keyboard_name = keyboard_name if keyboard_name is not None else MainApp.default_keyboard_name
		self.midiin = rtmidi.MidiIn()
		self.is_recording = False			#
		self.progression:Progression = None	#
		self.time:float = None		#
		self._called = False

	def __call__ (self):
		self._called = True
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
			# self.enter_listener_loop() #

	def __enter__ (self):
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self.midiin.__exit__(*sys.exc_info())

	@property
	def ports (self) -> list[str]:
		return self.midiin.get_ports()

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
				correlations = Correlations_in_kern_repository(str(self.progression))
							


		# what could be recorded:
		if self.is_recording and (msb == 0x90 or msb == 0x80):
			self.time += delta_time
			self.progression += Note(pitch, vel, self.time, delta_time)
			# print(pitch, vel, self.time, delta_time)	# my fail: passed by value or reference?
			# tag = f'<script>{self.progression}</script>'

	def enter_listener_loop (self):	# ...
		self.time = 0
		while True:
			pass