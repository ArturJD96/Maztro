class Sequence:

	# Manages toggling playback (not yet implemented) and recording of the midi input.

	def __init__ (self):
		self.records = False
		self.time = 0

	@property
	def records(self) -> bool:
		return self._records
	
	@records.setter
	def records(self, switch):
		self._records = switch
		if self._records:
			self.time = 0

	def toggle(self):
		self.records = not self._records