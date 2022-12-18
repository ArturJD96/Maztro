import typing
import unittest
import warnings
import shutup
import sys
import rtmidi

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

from Note import Note
from Progression import Progression
from MainApp import MainApp
from Utilities import Hardware_Warning

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class MidiNote_Tests(unittest.TestCase):

	def test_c_sharp_note_on (self):
		midi_note = Note(61, 100, 0.9)
		self.assertEqual('4c#', str(midi_note))

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

class Progression_tests(unittest.TestCase):

	def setUp(self):
		self.prog = Progression()
		progression = [	# this must be rewritten.
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
		result = '**midi\n48\n60\n72\n50\n62\n65\n69\n56\n58\n54\n49\n*-'
		self.mode = 'midi2humMidi'
		self.assertEqual(str(self.prog), result)

	def test_midi2humMidi_in_chord_mode (self):
		self.skipTest('Work In Progress')
		result = '**midi\n48\n60\n72\n50\n62\n65\n69\n56\n*^\n.\n58\n*v\n*v\n54\n49\n*-'
		self.mode = 'midi2humMidi'
		self.chord_mode = True
		self.assertEqual(str(self.prog), result)

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

#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

if __name__ == '__main__':
	unittest.main()