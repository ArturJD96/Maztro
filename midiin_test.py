from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #

import unittest

# # # # # # # # # # # # # # # # # # # # # # # # #

import rtmidi
import rtmidi.midiutil as midiutil 

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:

	defaultName = 'ArturBjörnApp_defaultName'

	def __init__(self, name:Optional[str] = None):
		self.isOpen = True
		self.name = Application.defaultName if name is None else name
		self.midiin = rtmidi.MidiIn(name = self.name)

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		pass

	def _get_rtmidiMidiIn_attr(self) -> rtmidi.MidiIn:
		for attr in self.__dict__:					#_!!! too long.
			appAttr = getattr(self, attr)
			if isinstance(appAttr, rtmidi.MidiIn):
				return appAttr
			else:
				None

# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

class AppTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.app = Application('Test')

	def test_if_App_opened_as_an_Application(self):
		assert isinstance(self.app, Application)

	def test_App_has_attribute_which_is_an_rtmidi_MidiIn(self):
		midiin = self.app._get_rtmidiMidiIn_attr()
		assert isinstance(midiin, rtmidi.MidiIn),\
			'The "app" object does not have a rtmidi.MidiIn attribute.'

	def test_App_has_default_name_if_no_name_provided(self):
		with Application() as app:
			assert app.name == Application.defaultName,\
				'The app has not assigned Application.defaultName as its default name.'


# # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()