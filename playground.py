def __call__ (self, event:tuple, data=None) -> None:	# ...
	
	# Define data
	midi, delta_t = event
	msb,pitch,vel = midi if len(midi) == 3 else (midi[0], None, None)

	# Actions for msb values triggering recording the sequence
	if msb in [250,251,252,0x99]:

		# Type
		if (msb == 0x99) and (pitch == 4) and (vel > 0):
			self.sequence.toggle()
		else:
			self.sequence.records = not (msb == 252)

		# Recording On (or Off)
		if self.sequence.records:
			print('RECORDING ON')
			self.progression = Progression()
			self.sequence.time = 0
		else:
			print(f'RECORDING OFF\n{self.progression}')
			print('KERN TO BE DISPLAYED AS INPUT:\n' + self.progression.get_display())
			if not self._offline:
				requests.post('http://127.0.0.1:5000', data = {"inputkern": str(self.progression)})
			correlations = Correlations_in_kern_repository(str(self.progression))

	elif self.sequence.records and (msb == 0x90 or msb == 0x80):
		self.time += delta_time
		self.progression += Note(pitch, vel, self.time, delta_time)
		# print(pitch, vel, self.time, delta_time)	# my fail: passed by value or reference?
		# tag = f'<script>{self.progression}</script>'