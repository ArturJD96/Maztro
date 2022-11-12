import typing

# # # # # # # # # # # # # # # # # # # # # # # # #

import unittest

# # # # # # # # # # # # # # # # # # # # # # # # #

import rtmidi
import rtmidi.midiutil as midiutil 

# # # # # # # # # # # # # # # # # # # # # # # # #

class Application:

	name = 'ArturBjörn'

	def __init__(self):
		self.isOpen = True
		self.name = Application.name
		self.midiin = rtmidi.MidiIn(name = self.name)

	def get_rtmidiMidiIn_attr(self) -> rtmidi.MidiIn:
		for attr in self.__dict__:					#_!!! too long.
			appAttr = getattr(self, attr)
			if isinstance(appAttr, rtmidi.MidiIn):
				return appAttr
			else:
				None

# # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # #

class AppTesting(unittest.TestCase):

	def testIfAppOpenedAsAnApplication(self):
		app = Application()
		assert isinstance(app, Application)

	def testAppHasAttributeWhichIsAnRtMidiMidiIn(self):
		app = Application()
		midiin = app.get_rtmidiMidiIn_attr()
		assert isinstance(midiin, rtmidi.MidiIn),\
			'The "app" object does not have a rtmidi.MidiIn attribute.'



# # # # # # # # # # # # # # # # # # # # # # # # #

# class MidiPortTesting (unittest.TestCase):

	# def testIfPortOpened(self):
	# 	with rtmidi.MidiIn(name = 'Midi In Test Port') as midiin:
	# 		print(midiin.get_ports())



# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()