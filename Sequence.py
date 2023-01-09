class Sequence:

	# Manages toggling playback (not yet implemented) and recording of the midi input.

	def __init__ (self):
		self.time = 0
		self._records = False
		self.callback_start_recording = None
		self.callback_stop_recording = None
		self.callback_when_event = None

	@property
	def records(self) -> bool:
		return self._records
	
	@records.setter
	def records(self, state):
		self._records = state
		if self._records:
			if self.callback_start_recording is not None:
				self.callback_start_recording()
			self.time = 0
		elif self.callback_stop_recording is not None:
			self.callback_stop_recording()

	def event (self, delta_time, event:tuple) -> None:
		if self.callback_when_event:
			self.time += delta_time
			self.callback_when_event(self.time, event)