import typing
import rtmidi

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Recording:

	str_mode = 'midi2humMidi'

	def __init__(self):
		self.midi = []

	def __str__(self):

		if Recording.str_mode == 'midi2humMidi':
			return self.midi2humMidi()

		elif Recording.str_mode == 'midi2kern':
			return self.midi2semits()


	def midi2kern(self):

		kern = '**kern\n'

		for midinote in self.midi:
			pitch, vel, deltaTime = midinote
			m = ((pitch-60) % 12)	# pitch class
			n = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b'][m] # pitch name
			n = n if pitch >= 60 else n.capitalize() # capitalize if below middle C
			o = abs(int((pitch/12)-5)) # calculate octave (0 is the octave of middle C)
			while o:
				n = n[0] + n # mark octave using humdrum note name repetition.
				o -= 1

			kern += '4' + str(n) + '\n'

		kern += '*-'

		return kern


	# def midi2semits(self):

	# 	kern = '**semits'

	# 	for i, midinote in enumerate(self.midi):

	# 		if i == 0:
	# 			kern += '0\n'
	# 		else:
	# 			kern += midinote[0] - 
	# 		print(midinote[0], i)

	# 	return kern


	def midi2humMidi(self):

		kern = '**midi\n'
		for midinote in self.midi:
			kern += f'{midinote[0]}\n'

		kern += '*-'

		return kern

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class App:

	is_recording = False
	recording:Recording = None

	def __init__(self):
		pass

	def __call__(self, event, data=None):

		midiMessage, deltaTime = event
		msb, pitch, vel = midiMessage

		msb_note_on = 153
		msb_note_off = 137

		key_recording = 4
		key_recording = 4

		if msb == msb_note_on and pitch == key_recording and vel > 0:
			App.is_recording = not App.is_recording
			if App.is_recording:
				print('RECORDING ON')
				App.recording = Recording()
			else:
				print('RECORDING OFF')
				print(App.recording)
		
		if App.is_recording and (msb == 144 or msb == 127):
			print(pitch, vel)
			App.recording.midi.append([pitch, vel, deltaTime])

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

with rtmidi.MidiIn() as midiin:

	keyboard_name = 'MPK mini 3'

	ports = midiin.get_ports()
	port_id = ports.index(keyboard_name)
	midiin.open_port(port_id)
	midiin.set_callback(App())

	while True:
		pass