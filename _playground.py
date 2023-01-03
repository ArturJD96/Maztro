import rtmidi
from rtmidi import midiutil
from timidity import play_notes
from collections import namedtuple
import numpy as np

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

Note = namedtuple('Note', ['pitch', 'velocity', 'start', 'end'])

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

def midi_callback (event, data):
	# [msb, pitch, vel], time = event
	# note = Note(pitch, vel, 0, 10)
	print(event)
	# play_notes([note], 120, 120, np.sin, wait_done=False)

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

with rtmidi.MidiIn() as midiout:

	port = midiout.open_port(0)
	midiout.set_callback(midi_callback)

	while True:
		pass