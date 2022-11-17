import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M I D I

import rtmidi
import rtmidi.midiutil as midiutil

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeys:

	'''
	This class contains the main body of the application.
	
	Statics:
	.default_keyboard_name [str]: name of the default hardware keyboard (must be in accord with it!).

	Attributes:
	.name [str]: name of the midi keyboard.
	.keyboard [rtmidi.MidiIn]: object handling midi in ports of the keyboard.
	._port_name: name of the midi in port returned by the .keyboard instantiation.
					Should be the same as .name!

	'''

	default_keyboard_name: str = 'MPK mini 3'

	def __init__(self, name:str=default_keyboard_name):

		self.name: str = name
		self.midiin: rtmidi.MidiIn; self._port_name: str
		self.midiin, self._port_name = midiutil.open_midiport(
			port  = None,
			type_ = "input",
			api   = rtmidi.API_UNSPECIFIED,
			use_virtual = True,
			interactive = False,
			client_name = 'Default Client Name APP_HCI',
			port_name   = self.name
		)

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		'''
		Every midi ports opened using class' attributes
		need to close when instance is teared down.
		'''
		self.midiin.delete()	# according to rtmidi docs: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn.delete

	@staticmethod
	def _choose_keyboard(midi_devices: list[str]=None) -> str:
		'''
		Returns name of MidiKeys object representing the default midi keyboard
		or – if not connected – computer keyboard.
		'''
		midi_ports: list[str] = midi_devices or rtmidi.MidiIn().get_ports()
		default_name = MidiKeys.default_keyboard_name
		return default_name if default_name in midi_ports else 'comp keyboard'