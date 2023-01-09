from Note import Note
from Progression import Progression
from MainApp import MainApp
from Utilities import Hardware_Warning

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

midi_in = ['MPK mini 3', 'Arturia BeatStep']

app = MainApp(midi_in[0], debug=True, offline=True)

app()