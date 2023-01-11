from Note import Note
from Progression import Progression
from MainApp import MainApp
from Utilities import Hardware_Warning

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

midi_in = ['MPK mini 3', 'Arturia BeatStep']

with MainApp(midi_in[0], debug=False, offline=True) as app:
	app()