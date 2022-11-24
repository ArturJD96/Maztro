import sys
import time
import logging

# logging.basicConfig(level=logging.DEBUG)

# import keyboard # for treating computer's keyboard as a midi keyboard.

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	T E S T I N G

import unittest
import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M I D I

import rtmidi
import rtmidi.midiutil as midiutil

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	T e s t e d   M o d u l e s

from Application import Application
from MidiIn import MidiIn
from MidiMessageHandler import MidiMessageHandler

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiIn_tests(unittest.TestCase):

	port_name = 'Testing_HCI_Midi_In'


	def setUp(self):
		self.midiin = MidiIn(MidiIn_tests.port_name)
		self.midiin_ports = rtmidi.MidiOut().get_ports()


	def tearDown(self):
		self.midiin.__exit__(*sys.exc_info()) # dummy args advised here: https://stackoverflow.com/questions/26635684/calling-enter-and-exit-manually


	def test_MidiIn_receives_default_port_name_if_no_name_provided(self):
		with MidiIn() as mk:
			assert mk.port_name in [MidiIn.default_device_name, MidiIn.software_port_name],\
				'The app does not have correct default name.'


	def test_port_name_provided_is_the_same_as_port_of_rtmidi_midiin(self):
		assert self.midiin.port_name == self.midiin._port_name,\
			'The rtmidi.MidiIn delegate uses different port name than provided when instantiating MidiIn object.'


	def test_check_if_default_device_is_connected(self):
		available_midiin_ports = [MidiIn.default_device_name]
		check = MidiIn.is_default_device_connected(available_midiin_ports)
		assert check,\
			'Default device is not detected despide being plugged.'


	def test_if_default_midi_device_is_plugged_choose_it_for_midiin_default(self):
		available_midiin_ports = ['port1', 'port2', MidiIn.default_device_name]
		chosen_device = MidiIn.get_default_device(available_midiin_ports)
		assert chosen_device == MidiIn.default_device_name,\
			'During instantiation of MidiIn, default midi device is not chosen despite being plugged.'


	def test_if_default_keyboard_is_NOT_plugged_choose_comp_keys_as_apps_keys(self):
		available_midi_ports = ['port1', 'port2']
		chosen_device = MidiIn.get_default_device(available_midi_ports)
		assert chosen_device == MidiIn.software_port_name,\
			'During MidiKeys instantiation, computer keyboard is not chosen as keyboard despite being the only valid midi source.'


	def test_only_one_default_midikeys_midiin_port_is_opened(self):
		port = MidiIn.default_device_name
		count = self.midiin_ports.count(port)
		assert count <= 1,\
			f'There are {count} default keyboard ports open, should be 1 or less.'


	def test_if_midikeys_opens_its_port(self):
		assert self.midiin.is_port_open(), 'The "app" didn\'t open its midiin port.'


	def test_is_midiin_port_visible_for_rtmidi_midiout_object(self):
		assert self.midiin.port_name in self.midiin_ports,\
			'MidiIn did not create a midi port visible for other rtmidi MidiOut object.'


	def test_if_midiin_returns_correct_index_of_its_port(self):
		available_midi_ports = ['port1', 'port2', MidiIn_tests.port_name, 'port3']
		assert self.midiin.get_port_id(available_midi_ports) == 2,\
			'.get_port_id method does not return correct index in the list of available ports.'


	def test_if_midiin_returns_correct_index_int(self):
		port_expected_id = self.midiin_ports.index(self.midiin.port_name)
		port_returned_id = self.midiin.get_port_id()
		assert port_returned_id == port_expected_id,\
			'.get_port_id method does not return correct index in the list of available ports.'


# # # # # # # # # # # # # # # # # # # # # # # # #

class Application_tests(unittest.TestCase):

	nameOfTheTestedApp = 'Test HCI_APP'


	def setUp(self):
		self.app = Application(Application_tests.nameOfTheTestedApp).__enter__()

	def tearDown(self):
		self.app.__exit__(*sys.exc_info()) # dummy args advised here: https://stackoverflow.com/questions/26635684/calling-enter-and-exit-manually


	def test_application_launches_with_its_default_name(self):
		with Application() as app:
			assert app.name == Application.default_name,\
				'When name argument is not given during instantiation, Application is not named according to its default name.'


	def test_if_app_opened_as_an_Application(self):
		assert isinstance(self.app, Application)


	def test_if_app_has_midiin(self):
		assert isinstance(self.app.midiin, MidiIn),\
			'The app"s "keyboard" is not of MidiKeys type.'


	def test_send_midi_message_and_receive_it_in_app(self):

		class Dummy:
			def __init__(self):
				self.flag = False
			def change_flag (self, event, data):
				self.flag = True

		testObject = Dummy()

		self.app.midiin.set_callback(testObject.change_flag)

		with rtmidi.MidiOut() as midiout:

			midiout.open_port(self.app.midiin.get_port_id())
			midiout.send_message([0x90, 48, 100]) # Note on [channel, note, vel]
			time.sleep(0.1)
			midiout.send_message([0x80, 48, 100]) # Note off
			time.sleep(0.1)

		assert testObject.flag,\
			'The midi message does not reach port of the MidiIn'


	def test_app_midiin_attr_has_callback_which_should_be_function(self):
		''' THIS TEST ALWAYS PASSES WHEN IT SHOULDNT. WHY ??? '''
		# This test should have failed before I implemented the callback itself.
		# Instead, it passed even though callback was not set.
		# The assertions showed, that under _callback there already is a callable.
		assert hasattr(self.app.midiin, '_callback'), 'No callback found.'
		assert callable(getattr(self.app.midiin, '_callback')), 'Callback is not assigned or is not a function.'

	# def test_app_midiin_callback_is_None_when_cancelled(self):
	# ''' IF WE REMOVE THE CALLBACK, THIS TEST SHOULD PASS AND IT DOES NOT !!! '''
	# self.app.midiin.cancel_callback()
	# assert self.app.midiin.callback is None,\
	# 	'Callback, when removed, is not of the None type.'

	# def test_if_midiin_attr_has_MidiMessageHandler_as_its_callback(self):
	# ''' THIS DOES NOT WORK ASS WELL... '''
	# 	assert isinstance(self.app.midiin._callback, MidiMessageHandler),\
	# 		'Callback of midiin attribute is not a MidiMessageHandler.'

	# the failure of the tests above do not allow me to check
	# if the midiin is set with the correct callback.
	def test_if_app_midi_callback_is_defined_as_MidiMessageHandler(self):
		assert isinstance(self.app.callback, MidiMessageHandler),\
			'App callback attribute is not a MidiMessageHandler.'

	def test_midi_cc_message_turns_on_recording(self):
		pass


# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiMessageInterpreter(unittest.TestCase):

	def setUp(self):
		self.mmi = MidiMessageHandler()

# # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':						# allows for opening as a script
	unittest.main()