import sys

import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M O D U L E S

from MidiIn import MidiIn
from MidiMessageHandler import MidiMessageHandler

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

	def __init__(self, name:str=None):
		
		self.name = name or Application.default_name
		self.midiin = MidiIn()	# open midi in port
		self.callback = MidiMessageHandler(self.midiin.port_name)

		self.midiin.set_callback(self.callback) #_! this is not covered in tests!

		# on initialization:
		# — open keyboard's port (on attribute instantiation)
		# – attach callback. Callback is a method of Application ?
		# ... continue with instantiation ...
		# – run the main loop ???
		#	* create debug attribute. If true, run loop but stop it soon (?). If false, run it.

		# -> Recording

		# -> move to self.keyborad self.recordingOn
		# self.keyboard.recording
		# while keyboard.recordingOn:

	def __enter__(self):
		self.midiin.__enter__()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		'''
		Every midi ports opened using class' attributes
		need to close when instance is teared down.
		'''
		self.midiin.__exit__(*sys.exc_info())	# according to rtmidi docs: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn.delete