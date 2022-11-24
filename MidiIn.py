import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M I D I

import rtmidi
import rtmidi.midiutil as midiutil

# # # # # # # # # # # # # # # # # # # # # # # # #

class MidiIn:
	
	'''
	This class handles the midi in port of the application.
	It delegates all the midi transfer and port handling
	to the rtmidi.MidiIn() class.

	[Log:] I cannot make this class to simply inherit from
	rtmidi.MidiIn() due to the way how the latter handles
	instantiation (using Cython's __cinit__):
	  – Even if I override childs __init__, the argument checks
	  	keep refering to the parent's __cinit__.
	  – I did not succeed with overriding __cinit__.
	    Some insight is provided here: https://stackoverflow.com/questions/47624000/cinit-takes-exactly-2-positional-arguments-when-extending-a-cython-class

	"Delegate" means, that every call for a method
	that cannot be find in the MidiIn class itself
	will be handled by the rtmidi.MidiIn class.
	
	Statics:
	.default_device_name[str] — name of the default hardware keyboard (must be in accord with it!).

	Attributes:
	.port_name [str] — name of the midi keyboard.

	Private Attributes:
	._midiin – delegate to the rtmidi.MidiIn class.

	'''

	default_device_name:str = 'MPK mini 3'
	software_port_name:str = 'comp keyboard'
	default_client_name:str = 'Default Client Name APP_HCI'

	@staticmethod
	def is_default_device_connected(ports:list[str]=None) -> bool:
		return MidiIn.default_device_name in (ports or rtmidi.MidiIn().get_ports())

	@staticmethod		
	def get_default_device(ports:list[str]=None) -> str:
		'''Returns name of the default hardware device or – if not connected – software device'''
		return MidiIn.default_device_name if MidiIn.is_default_device_connected(ports) else  MidiIn.software_port_name

	''' i n s t a n c e   m e t h o d s'''

	def __init__(self, name:str=None):

		self.port_name:str = name or MidiIn.get_default_device()

		# DELEGATE [https://erikscode.space/index.php/2020/08/01/delegate-and-decorate-in-python-part-1-the-delegation-pattern/]
		self._midiin:rtmidi.MidiIn; self._port_name:str
		self._midiin, self._port_name = midiutil.open_midiport(
			port  = None,
			type_ = "input",
			api   = rtmidi.API_UNSPECIFIED,
			use_virtual = True,
			interactive = False,
			client_name = MidiIn.default_client_name,
			port_name   = self.port_name
		)
		self._midiin_methods:list[str] = [m for m in dir(rtmidi.MidiIn) if not m.startswith('_')]

	def __getattr__(self, func):
		'''delegates rtmidi.MidiIn methods'''
		def method(*args):
			if func in self._midiin_methods:
				return getattr(self._midiin, func)(*args)
			else:
				raise AttributeError

		return method

	def __enter__(self):
		self._midiin.__enter__() # opens the port as well.
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self._midiin.__exit__(exception_type, exception_value, traceback)