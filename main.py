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

class Recording:

	def __init__(self):
		self.midi = []
		self.mode = 'midi2humMidi'

	def __str__(self):
		match self.mode:
			case 'midi2humMidi':
				return self.midi2humMidi()
			case 'midi2kern':
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

			# check if this works:
			# kern = '**midi' + (note for note in self.midi) + '*-'

		kern += '*-'

		return kern

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#



#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

# with rtmidi.MidiIn() as midiin:

# 	keyboard_name = 'MPK mini 3'

# 	ports = midiin.get_ports()
# 	port_id = ports.index(keyboard_name)
# 	midiin.open_port(port_id)
# 	midiin.set_callback(App())

# 	while True:
# 		pass

class MainApp:

	default_keyboard_name = 'MPK mini 3'

	def __enter__ (self):
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self.midiin.__exit__()
		pass

	def __init__ (self, keyboard_name:str=None):
		self.keyboard_name = keyboard_name if keyboard_name is not None else MainApp.default_keyboard_name
		self.midiin = rtmidi.MidiIn()
		self.is_recording = False			#
		self.recording:Recording = None		#
		self._called = False

	def __call__ (self):
		self._called = True
		self.midiin.open_virtual_port(self.keyboard_name)
		self.midiin.set_callback(self.handle_incoming_midi, self)
		try:
			port_id:int = self.midiin.get_ports().index(self.keyboard_name)
			with self.midiin.open_port(port_id):
				self.enter_listener_loop() #

		except ValueError as ve:
			keyboard_name = MainApp.default_keyboard_name
			if ve.args[0] == f"'{keyboard_name}' is not in list":
				warnings.warn(
					f"{keyboard_name} is not connected. Use your computer keyboard as midi keyboard.",
					Hardware_Warning)
		else:
			# listen to the keyboard strokes !
			with self.midiin.open_virtual_port(self.keyboard_name):
				self.enter_listener_loop() #


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
				self.recording = Recording()
			else:
				print('RECORDING OFF\n', self.recording)
		if self.is_recording and (msb == 0x90 or msb == 0x80):
			print(pitch, vel)
			self.recording.midi.append([pitch, vel, deltaTime])


	def enter_listener_loop (self):	# ...
		while False:
			pass


#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MainApp_tests(unittest.TestCase):

	def setUp(self):
		shutup.mute_warnings()
		self.app = MainApp().__enter__()
		self.app()

	def tearDown(self):
		shutup.unmute_warnings() # unmute warnings
		self.app.__exit__(*sys.exc_info())
		del self.app	# according to rtmidi docs: https://spotlightkid.github.io/python-rtmidi/rtmidi.html#rtmidi.MidiIn.delete)

	def test_app_is_instance_of_MainApp(self):
		self.assertIsInstance(self.app, MainApp)

	def test_app_defaul_keyboard_name_is_defined(self):
		self.assertIsNotNone(MainApp.default_keyboard_name)

	def test_app_is_callable(self):
		self.assertTrue(callable(self.app))

	def test_is_apps_toggle_on(self):
		self.assertTrue(self.app._called)

	def test_keyboard_name_attr_when_no_keyboard_name_provided(self):
		self.assertEqual(self.app.keyboard_name, MainApp.default_keyboard_name)

	def test_keyboard_name_attr_when_name_provided(self):
		keyboard_name = 'testing keyboard'
		app = MainApp(keyboard_name)
		self.assertEqual(app.keyboard_name, keyboard_name)

	def test_app_midi_port_is_open(self):
		self.assertTrue(self.app.midiin.is_port_open())

	def test_app_keyboard_name_is_among_midiin_ports_only_once(self):
		midiin_ports = rtmidi.MidiOut().get_ports() # MidiOut seeks for MidiIn ports (and vice versa).
		count = midiin_ports.count(self.app.keyboard_name)
		self.assertEqual(count, 1)

	def test_app_with_its_default_keyboard_warns_if_this_keyboard_is_not_connected(self):
		app = MainApp(MainApp.default_keyboard_name)
		expected_error_message = f'{MainApp.default_keyboard_name} is not connected. Use your computer keyboard as midi keyboard.'
		warnings.warn(expected_error_message, Hardware_Warning, stacklevel=2)
		with self.assertWarnsRegex(Hardware_Warning, expected_error_message):
			shutup.unmute_warnings()
			app()


if __name__ == '__main__':
	unittest.main()

