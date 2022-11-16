import time
import keyboard
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

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeys:

	default_keyboard_name: str = 'Akai Mini MPK 3'

	def __init__(self, name:Optional[str]=None):

		self.name: str = name or MidiKeys.default_keyboard_name

		self.midiin: rtmidi.MidiIn
		self._port_name: str
		self.midiin, self._port_name = midiutil.open_midiport(
			port  = None,
			type_ = "input",
			api   = rtmidi.API_UNSPECIFIED,
			use_virtual = True,
			interactive = False,
			client_name = Application.default_name,
			port_name   = self.name
		)

	def _get_rtmidiMidiIn_attr(self) -> rtmidi.MidiIn:
		for attr in self.__dict__:					#_! too long.
			appAttr = getattr(self, attr)
			if isinstance(appAttr, rtmidi.MidiIn):
				return appAttr
			else:
				continue

	@staticmethod
	def _choose_keyboard(midi_devices: list[str]=None) -> 'MidiKeys':	#_! string, because bare MidiKeys is not recognized as type...
		
		midi_ports: list[str] = midi_devices or rtmidi.MidiIn().get_ports()

		if MidiKeys.default_keyboard_name in midi_ports:

			return MidiKeys(MidiKeys.default_keyboard_name)

		else:

			#_! Create MidiKeys instance which represents computer keyboard...
			return MidiKeys('comp keyboard')

	def __enter__(self):
		pass

	def __exit__(self, exception_type, exception_value, traceback):
		pass

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:

	default_name: str = 'ArturBjörnApp_defaultName'

	def __init__(self, name:Optional[str]=None):

		self.isOpen = True
		self.name = Application.default_name if name is None else name
		self.keyboard = MidiKeys._choose_keyboard()

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		pass

# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeysTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.midikeys = MidiKeys('TestMidiKeys')

	def test_has_attribute_which_is_an_rtmidi_MidiIn(self):
		midiin = self.midikeys._get_rtmidiMidiIn_attr()
		assert isinstance(midiin, rtmidi.MidiIn),\
			'The "MidiKeys" object does not have a rtmidi.MidiIn attribute.'

	def test_if_midiKeys_opens_its_port(self):
		assert self.midikeys.midiin.is_port_open(), 'The "app" didn\'t open its midiin port.'

	def test_app_receives_default_name_if_no_name_provided(self):
		midikeys = MidiKeys()
		assert midikeys.name == midikeys.default_keyboard_name,\
			'The app has not Application.defaultName as its default name.'

	def test_if_port_name_is_the_same_as_apps(self):
		port_name_provided = self.midikeys.name
		port_name_returned = self.midikeys._port_name
		assert port_name_provided == port_name_returned, 'Port name does not match the name app provided.'

	def test_choose_keyboard_static_method_returns_MidiKeys_if_called_without_arguments(self):
		assert MidiKeys()._choose_keyboard()

	def test_if_default_keyboard_is_plugged_choose_it_as_apps_keys(self):
		available_midi_ports = [ 'port1', 'port2', MidiKeys.default_keyboard_name ]
		chosen_keyboard = MidiKeys._choose_keyboard(available_midi_ports)
		assert chosen_keyboard.name == MidiKeys.default_keyboard_name,\
			'During MidiKeys instantiation, default midi keyboard is not chosen as keyboard source despite being plugged.'

	def test_if_default_keyboard_is_NOT_plugged_choose_comp_keys_as_apps_keys(self):
		available_midi_ports = [ 'port1', 'port2' ]
		chosen_keyboard = MidiKeys._choose_keyboard(available_midi_ports)
		assert chosen_keyboard.name == 'comp keyboard',\
			'During MidiKeys instantiation, computer keyboard is not chosen as keyboard despite being the only valid midi source.'

# # # # # # # # # # # # # # # # # # # # # # # # #

class ApplicationTests(unittest.TestCase):

	nameOfTheTestedApp = 'Test HCI_APP'

	@classmethod
	def setUpClass(self):
		self.app = Application(ApplicationTests.nameOfTheTestedApp)

	def test_if_app_opened_as_an_Application(self):
		assert isinstance(self.app, Application)

	def test_if_app_sees_keyboard_which_is_MidiKeys_object(self):
		assert type(self.app.keyboard) == MidiKeys,\
			'The app"s "keyboard" is not of MidiKeys type.'

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()