import rtmidi

def dummyCallback(arg1, arg2):
	print('dummy')
	print(arg1)
	print(arg2)


with rtmidi.MidiIn() as midiin:

	midiin.open_port(0)
	midiin.set_callback(dummyCallback)

	while True:
		pass