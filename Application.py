import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M O D U L E S

from MidiKeys import MidiKeys

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:
	
	'''
	This class contains the main body of the application.
	
	Statics:
	.default_name [str]: default name for the whole application.

	Attributes:
	.name [str]: name of the whole Application
	.keyboard [rtmidi.MidiIn]: object representing a hardware virtual keyboard

	'''

	default_name: str = 'ArturBjörnApp_defaultName'

	def __init__(self, name:[str]=default_name):
		self.name = name
		self.keyboard = MidiKeys()

	def __enter__(self):
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		'''
		Every midi ports opened using class' attributes
		need to close when instance is teared down.
		'''
		self.keyboard.midiin.delete()	# according to rtmidi docs: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn.delete