import typing
import unittest
import warnings
import shutup
import sys

import rtmidi

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Hardware_Warning(Warning):
	pass


#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Note:

	names = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b']

	def __init__ (self, pitch, velocity, delta_time):	# as midi note
		self.pitch = pitch
		self.velocity = velocity
		self.duration = delta_time

	def __str__ (self):									# as humdrum token
		m = ((self.pitch-60) % 12)	# pitch class
		n = Note.names[m] # pitch name
		n = n if self.pitch >= 60 else n.capitalize() # capitalize if below middle C
		o = abs(int((self.pitch/12)-5)) # calculate octave (0 is the octave of middle C)
		while o:
			n = n[0] + n # mark octave using humdrum note name repetition.
			o -= 1
		return '4' + str(n)	

class MidiNote_Tests(unittest.TestCase):

	def test_c_sharp_note_on (self):
		midi_note = Note(61, 100, 0.9)
		self.assertEqual('4c#', str(midi_note))


#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression:

	def __init__ (self):
		self.notes = [] # array of tuples
		self.mode = 'midi2humMidi'

	def __str__ (self):
		match self.mode:
			case 'midi2humMidi':
				return self.midi2humMidi()
			case 'midi2kern':
				return self.midi2semits()

	def __iadd__ (self, note:Note):
		self.notes.append(note)
		return self

	def midi2kern(self):

		kern = '**kern\n'

		for midi_note_on in self.notes:

			pitch, vel, deltaTime = midi_note_on
			m = ((pitch-60) % 12)	# pitch class
			n = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b'][m] # pitch name
			n = n if pitch >= 60 else n.capitalize() # capitalize if below middle C
			o = abs(int((pitch/12)-5)) # calculate octave (0 is the octave of middle C)
			while o:
				n = n[0] + n # mark octave using humdrum note name repetition.
				o -= 1

			kern += '4' + str(n) + '\n'

		kern += '*-'

		'''
		spines = []
		for midi_note_on in self.midi:
			pitch, vel, delta_time = midi_note_on
			if vel:
				spines.append(0)
				m = ((pitch-60) % 12)	# pitch class
				n = ['c','c#','d','e–','e','f','f#','g','a–','a','b–','b'][m] # pitch name
				n = n if pitch >= 60 else n.capitalize() # capitalize if below middle C
				o = abs(int((pitch/12)-5)) # calculate octave (0 is the octave of middle C)
				while o:
					n = n[0] + n # mark octave using humdrum note name repetition.
					o -= 1
			else:
				spines. # remove the currently pointed spine and mark it by putting *v
		'''

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
		spine = ''.join(f'{n.pitch}\n' for n in self.notes if n.velocity > 0)
		return '**midi\n' + spine + '*-'


#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#


class MainApp:

	default_keyboard_name = 'MPK mini 3'

	def __enter__ (self):
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self.midiin.__exit__(*sys.exc_info())

	def __init__ (self, keyboard_name:str=None):
		self.keyboard_name = keyboard_name if keyboard_name is not None else MainApp.default_keyboard_name
		self.midiin = rtmidi.MidiIn()
		self.is_recording = False			#
		self.progression:Progression = None		#
		self._called = False

	def __call__ (self):
		self._called = True
		self.midiin.set_callback(self.handle_incoming_midi, self)
		try:
			port_id:int = self.ports.index(self.keyboard_name)
			self.midiin.open_port(port_id)
			self.enter_listener_loop() #

		except ValueError as ve:
			keyboard_name = MainApp.default_keyboard_name
			if ve.args[0] == f"'{keyboard_name}' is not in list":
				warnings.warn(
					f"{keyboard_name} is not connected. Use your computer keyboard as midi keyboard.",
					Hardware_Warning)
			# listen to the keyboard strokes !
			self.midiin.open_virtual_port(self.keyboard_name)
			#self.enter_listener_loop() #

	@property
	def ports (self):
		return self.midiin.get_ports()

	def handle_incoming_midi (self, event:tuple, data=None) -> None:	# ...
		msb_note_on  = 0x99
		msb_note_off = 0x89
		key_recording = 4
		key_recording = 4
		midi_message, delta_time = event
		msb, pitch, vel = midi_message
		if msb == msb_note_on and pitch == key_recording and vel > 0:
			self.is_recording = not self.is_recording # toggle
			if self.is_recording:
				print('RECORDING ON')
				self.progression = Progression()
			else:
				print('RECORDING OFF\n', self.progression)
		if self.is_recording and (msb == 0x90 or msb == 0x80):
			print(pitch, vel, delta_time)
			note = Note(pitch, vel, delta_time)
			self.progression += addNote(note)


	def enter_listener_loop (self):	# ...
		while False:
			pass


#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression_tests(unittest.TestCase):

	# def midi2humMidi(self):

	# 	kern = '**midi\n'
	# 	for midinote in self.midi:
	# 		kern += f'{midinote[0]}\n'

	# 		# check if this works:
	# 		# kern = '**midi' + (note for note in self.midi) + '*-'

	# 	kern += '*-'

	# 	return kern

	def setUp(self):
		self.prog = Progression()
		progression = [
			(48, 38, 1.7640808810000002),
			(48, 0, 0.166371539),
			(60, 59, 0.970119562),
			(60, 0, 0.175734614),
			(72, 74, 0.16370496),
			(72, 0, 0.17179357),
			(50, 53, 0.849966957),
			(50, 0, 0.17900775100000002),
			(62, 51, 0.050158615000000004),
			(62, 0, 0.179213711),
			(65, 54, 0.030622804000000003),
			(65, 0, 0.147462531),
			(69, 60, 0.133557157),
			(69, 0, 0.17826818800000002),
			(56, 107, 0.8804223720000001),
			(58, 54, 0.49278880700000005),
			(56, 0, 0.0038723980000000004),
			(58, 0, 0.5838593510000001),
			(54, 62, 0.012881354000000001),
			(54, 0, 0.458346203),
			(49, 127, 4.308793076000001),
			(49, 0, 0.104754516)
		]
		for t in progression:
			note = Note(t[0], t[1], t[2])
			self.prog += note

	def test_midi2humMidi (self):
		result = '**midi\n48\n48\n60\n60\n72\n72\n50\n50\n62\n62\n65\n65\n69\n69\n56\n58\n56\n58\n54\n54\n49\n49\n*-'
		result2 = '**midi\n48\n60\n72\n50\n62\n65\n69\n56\n58\n54\n49\n*-'
		self.mode = 'midi2humMidi'
		self.assertEqual(str(self.prog), result2)



#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MainApp_tests(unittest.TestCase):

	def setUp (self):
		shutup.mute_warnings()
		self.app = MainApp()
		self.app()

	def tearDown (self):
		shutup.unmute_warnings() # unmute warnings
		self.app.__exit__(*sys.exc_info())
		del self.app	# according to rtmidi docs: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn.delete)

	def test_app_is_instance_of_MainApp (self):
		self.assertIsInstance(self.app, MainApp)

	def test_app_defaul_keyboard_name_is_defined (self):
		self.assertIsNotNone(MainApp.default_keyboard_name)

	def test_app_is_callable (self):
		self.assertTrue(callable(self.app))

	def test_is_apps_toggle_on (self):
		self.assertTrue(self.app._called)

	def test_keyboard_name_attr_when_no_keyboard_name_provided (self):
		self.assertEqual(self.app.keyboard_name, MainApp.default_keyboard_name)

	def test_keyboard_name_attr_when_name_provided (self):
		keyboard_name = 'testing keyboard'
		app = MainApp(keyboard_name)
		self.assertEqual(app.keyboard_name, keyboard_name)

	def test_app_midi_port_is_open (self):
		self.assertTrue(self.app.midiin.is_port_open())

	def test_app_keyboard_name_is_among_midiin_ports_only_once (self):
		midiin_ports = rtmidi.MidiOut().get_ports() # MidiOut seeks for MidiIn ports (and vice versa).
		count = midiin_ports.count(self.app.keyboard_name)
		self.assertEqual(count, 1)

	def test_app_warns_if_default_keyboard_is_not_connected (self):
		if MainApp.default_keyboard_name in self.app.ports:
			self.skipTest('Cannot test absence of the default keyboard when default keyboard is connected.')
		shutup.unmute_warnings()
		app = MainApp()
		expected_error_message = f'{MainApp.default_keyboard_name} is not connected. Use your computer keyboard as midi keyboard.'
		warnings.warn(expected_error_message, Hardware_Warning, stacklevel=2)
		with self.assertWarnsRegex(Hardware_Warning, expected_error_message):
			app()

if __name__ == '__main__':
	unittest.main()