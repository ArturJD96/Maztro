import rtmidi
from _rtmidi_copy import MidiBase

def mockFunc ():
	print('Mocked.')

with rtmidi.MidiIn() as midiin:

	midiin.open_virtual_port("Playground_Port")

	midiin.set_callback(mockFunc)

	assert callable(midiin._callback)