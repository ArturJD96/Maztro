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
from MidiListener import MidiListener
from Utilities import Hardware_Warning
from Correlations import Correlations_in_kern_repository

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MainApp:

	default_keyboard_name = 'MPK mini 3'

	def __init__ (self, keyboard_name:str=None, debug:bool=False, offline:bool=False):
		self.keyboard_name = keyboard_name if keyboard_name is not None else MainApp.default_keyboard_name

		self.midiin = rtmidi.MidiIn()
		self.sequence = Sequence()
		self.listener = MidiListener(self.sequence, debug=debug, offline=offline)

		self._debug:bool = debug # outputs mock midi input for testing purposes when keyboard no keyboard detected
		self._offline:bool = offline # turns off posting requests in handle_incoming_midi method (the midi listener func).

	@property
	def ports (self) -> list[str]:
		return self.midiin.get_ports()

	def __call__ (self):

		self.midiin.set_callback(self.listener, self)

		try:
			port_id:int = self.ports.index(self.keyboard_name)
			self.midiin.open_port(port_id)

		except ValueError as ve:
			keyboard_name = MainApp.default_keyboard_name
			if ve.args[0] == f"'{keyboard_name}' is not in list":
				warnings.warn(
					f"{keyboard_name} is not connected. Use your computer keyboard as midi keyboard.",
					Hardware_Warning)
			# listen to the keyboard strokes !
			self.midiin.open_virtual_port(self.keyboard_name)

		MidiListener.activate(self.listener, debug=self._debug) # ENTER NON-ASYNC LISTENER LOOP

	def __enter__ (self):
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self.midiin.__exit__(*sys.exc_info())