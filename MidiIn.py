import typing
from typing import Optional

# # # # # # # # # # # # # # # # # # # # # # # # #
#
#	M I D I

import rtmidi
import rtmidi.midiutil as midiutil



# # # # # # # # # # # # # # # # # # # # # # # # #

'''
CLASS: M i d i  I n

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

class MidiIn:

	default_device_name:str = 'MPK mini 3'
	software_port_name:str = 'comp keyboard' # dummy
	default_client_name:str = 'Default Client Name APP_HCI' # dummy

	@staticmethod
	def is_default_device_connected(ports:list[str]=None) -> bool:
		return MidiIn.default_device_name in (ports or rtmidi.MidiIn().get_ports())

	@staticmethod		
	def get_default_device(ports:list[str]=None) -> str:
		'''Returns name of the default hardware device or – if not connected – software device'''
		return MidiIn.default_device_name if MidiIn.is_default_device_connected(ports) else MidiIn.software_port_name


	''' i n s t a n c e   m e t h o d s'''

	def __init__ (self, name:str=None):

		self.port_name:str = name or MidiIn.get_default_device()

		# rtmidi.MidiIn delegate [https://erikscode.space/index.php/2020/08/01/delegate-and-decorate-in-python-part-1-the-delegation-pattern/]
		self._midiin = rtmidi.MidiIn()
		self._midiin_methods:list[str] = [m for m in dir(rtmidi.MidiIn) if not m.startswith('_')]


	def get_port_id (self, ports:list[str]=None) -> Optional[int]:
		ports = ports or rtmidi.MidiOut().get_ports()
		return ports.index(self.port_name) if self.port_name in ports else None


	def __getattr__ (self, func):
		'''delegates rtmidi.MidiIn methods'''
		def method(*args):
			if func in self._midiin_methods:
				return getattr(self._midiin, func)(*args)
			else:
				raise AttributeError
		return method


	def __enter__ (self):
		self._midiin.__enter__()
		if self.port_name == MidiIn.default_device_name:
			self.open_port(self.get_port_id(), self.port_name)
		else:	
			self.open_virtual_port(self.port_name)
		return self

	def __exit__ (self, exception_type, exception_value, traceback):
		self._midiin.__exit__(exception_type, exception_value, traceback)
		self.close_port()
		self.delete()