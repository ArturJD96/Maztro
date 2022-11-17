import sys
import time
# import keyboard # for treating computer's keyboard as a midi keyboard.
from copy import copy

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	T E S T I N G

import unittest
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M I D I

import rtmidi
import rtmidi.midiutil as midiutil

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeys:

	default_keyboard_name: str = 'MPK mini 3'

	def __init__(self, name:Optional[str]=None):

		self.name: str = name or MidiKeys._choose_keyboard()
		self.midiin: rtmidi.MidiIn; self._port_name: str
		self.midiin, self._port_name = midiutil.open_midiport(
			port  = None,
			type_ = "input",
			api   = rtmidi.API_UNSPECIFIED,
			use_virtual = True,
			interactive = False,
			client_name = Application.default_name,
			port_name   = self.name
		)

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.midiin.delete()

	@staticmethod
	def _choose_keyboard(midi_devices: list[str]=None) -> str:
		'''
		Returns name of MidiKeys object representing the default midi keyboard
		or – if not connected – computer keyboard.
		'''
		midi_ports: list[str] = midi_devices or rtmidi.MidiIn().get_ports()
		default_name = MidiKeys.default_keyboard_name
		return default_name if default_name in midi_ports else 'comp keyboard'

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:

	default_name: str = 'ArturBjörnApp_defaultName'

	def __init__(self, name:Optional[str]=None):

		self.isOpen = True
		self.name = Application.default_name if name is None else name
		self.keyboard = MidiKeys()

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.keyboard.midiin.delete()

# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeysTests(unittest.TestCase):

	def setUp(self):
		self.midikeys = MidiKeys('TestMidiKeys').__enter__()
		self.midiout = rtmidi.MidiOut()

	def tearDown(self):
		self.midikeys.__exit__(*sys.exc_info()) # dummy args advised here: https://stackoverflow.com/questions/26635684/calling-enter-and-exit-manually

	def test_has_attribute_which_is_an_rtmidi_MidiIn(self):
		midiin_attr = None 
		for attr in self.midikeys.__dict__:			#_! too long...
			appAttr = getattr(self.midikeys, attr)
			if isinstance(appAttr, rtmidi.MidiIn):
				midiin_attr = appAttr
				break
		assert isinstance(midiin_attr, rtmidi.MidiIn),\
			'The "MidiKeys" object does not have a rtmidi.MidiIn attribute.'

	def test_if_midikeys_opens_its_port(self):
		assert self.midikeys.midiin.is_port_open(), 'The "app" didn\'t open its midiin port.'

	def test_app_receives_default_name_if_no_name_provided(self):
		with MidiKeys() as mk:
			assert mk.name in [mk.default_keyboard_name, 'comp keyboard'],\
				'The app has not Application.defaultName as its default name.'

	def test_if_port_name_is_the_same_as_apps(self):
		port_name_provided = self.midikeys.name
		port_name_returned = self.midikeys._port_name
		assert port_name_provided == port_name_returned, 'Port name does not match the name app provided.'

	def test_choose_keyboard_static_method_returns_MidiKeys_if_called_without_arguments(self):
		with MidiKeys() as mk:
			assert mk._choose_keyboard()

	def test_if_default_keyboard_is_plugged_choose_it_as_apps_keys(self):
		available_midi_ports = [ 'port1', 'port2', MidiKeys.default_keyboard_name ]
		chosen_keyboard = MidiKeys._choose_keyboard(available_midi_ports)
		assert chosen_keyboard == MidiKeys.default_keyboard_name,\
			'During MidiKeys instantiation, default midi keyboard is not chosen as keyboard source despite being plugged.'

	def test_if_default_keyboard_is_NOT_plugged_choose_comp_keys_as_apps_keys(self):
		available_midi_ports = [ 'port1', 'port2' ]
		chosen_keyboard = MidiKeys._choose_keyboard(available_midi_ports)
		assert chosen_keyboard == 'comp keyboard',\
			'During MidiKeys instantiation, computer keyboard is not chosen as keyboard despite being the only valid midi source.'

	def test_only_one_default_midikeys_midiin_port_is_opened(self):
		port = MidiKeys.default_keyboard_name
		midiin_ports = self.midiout.get_ports()
		count = midiin_ports.count(port)
		assert count <= 1,\
			f'There are {count} default keyboard ports open, should be 1 or less.'

	def test_is_midikeys_port_visible_for_rtmidi_midiout_object(self):
		ports = self.midiout.get_ports()
		assert self.midikeys.name in ports,\
			'MidiKeys midiin did not create a midi port visible for other rtmidi MidiOut object.'
		

# # # # # # # # # # # # # # # # # # # # # # # # #

class ApplicationTests(unittest.TestCase):

	nameOfTheTestedApp = 'Test HCI_APP'

	def setUp(self):
		self.app = Application(ApplicationTests.nameOfTheTestedApp).__enter__()

	def tearDown(self):
		self.app.__exit__(*sys.exc_info()) # dummy args advised here: https://stackoverflow.com/questions/26635684/calling-enter-and-exit-manually

	def test_if_app_opened_as_an_Application(self):
		assert isinstance(self.app, Application)

	def test_if_app_sees_keyboard_which_is_MidiKeys_object(self):
		assert type(self.app.keyboard) == MidiKeys,\
			'The app"s "keyboard" is not of MidiKeys type.'

# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()