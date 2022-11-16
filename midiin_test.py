import time

# # # # # # # # # # # # # # # # # # # # # # # # #

import unittest
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #

import rtmidi
import rtmidi.midiutil as midiutil 

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeys:

	default_keyboard: str = 'Akai Mini MPK 3'

	def __init__(self, name:Optional[str]=None):

		self.name: str = name or MidiKeys.default_keyboard

		self.midiin: rtmidi.MidiIn
		self.port_name: str
		self.midiin, self.port_name = rtmidi.midiutil.open_midiport(
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

	def __enter__(self):
		pass

	def __exit__(self, exception_type, exception_value, traceback):
		pass

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:

	default_name = 'ArturBjörnApp_defaultName'

	def __init__(self, name:Optional[str]=None):

		self.isOpen = True
		self.name = Application.default_name if name is None else name

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		pass

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiKeysTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.midiKeys = MidiKeys('TestMidiKeys')

	def test_has_attribute_which_is_an_rtmidi_MidiIn(self):
		midiin = self.midiKeys._get_rtmidiMidiIn_attr()
		assert isinstance(midiin, rtmidi.MidiIn),\
			'The "MidiKeys" object does not have a rtmidi.MidiIn attribute.'

	def test_if_midiKeys_opens_its_port(self):
		assert self.midiKeys.midiin.is_port_open(), 'The "app" didn\'t open its midiin port.'

	def test_app_receives_default_name_if_no_name_provided(self):
		midikeys = MidiKeys()
		assert midikeys.name == midikeys.default_keyboard,\
			'The app has not Application.defaultName as its default name.'

	# def test_if_port_name_is_the_same_as_apps(self):
	# 	port_name_provided = self.app.keyboard.name
	# 	port_name_returned = self.app.name
	# 	assert port_name_provided == port_name_returned, 'Port name does not match the name app provided.'

# # # # # # # # # # # # # # # # # # # # # # # # #

class AppTest(unittest.TestCase):

	nameOfTheTestedApp = 'Test HCI_APP'

	@classmethod
	def setUpClass(self):
		self.app = Application(AppTest.nameOfTheTestedApp)

	def test_if_app_opened_as_an_Application(self):
		assert isinstance(self.app, Application)

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()