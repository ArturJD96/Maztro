# coding=utf-8
import os
import platform
import subprocess

class Correlations_in_kern_repository:

	CORRELATION_MINIMUM = 0.4

	def __init__ (self, kern_input:str=None, kern_repository_directory:str=None):

		if kern_input is not None:
			if not isinstance(kern_input, str): raise Exception("Argument 'kern input' must be a string!")
		if kern_repository_directory is not None:
			if not isinstance(kern_repository_directory, str): raise Exception("Argument 'kern repository directory' must be a string!")

		self.humdrum_directory, self.input_file_name, self.wsl = self.selectPlatform()
		kern_repo_dir = kern_repository_directory or f"{self.humdrum_directory}/data/mozart/piano-sonatas/kern"

		self.dict = { piece : self.get_correlated_bars(f'{kern_repo_dir}/{piece}') for piece in os.listdir(kern_repo_dir) }


	def get_correlated_bars (self, kern_piece_dir: str):

		if not isinstance(kern_piece_dir, str): raise Exception("Argument 'kern_piece_dir' must be a string!")
		print(f'checking {kern_piece_dir}')
		with\
			open(kern_piece_dir, 'r') as file,\
			open('input.semits', 'w') as input_semits,\
			open('mozart.semits', 'w') as sonata_semits,\
			open('sonataLeftSpine.semits', 'w') as sonata_left_spine_semits,\
			open('sonataLeftColumn.semits', 'w') as sonata_left_column_semits,\
			open('sonataLeftColumn.correl', 'w') as sonata_left_column_correl:
			
			subprocess.run(['semits', '-x', self.input_file_name], stdout=input_semits)
			subprocess.run(['semits', '-x', kern_piece_dir], stdout=sonata_semits)
			subprocess.run(['extract', '-p', '1', 'mozart.semits'], stdout=sonata_left_spine_semits)
			subprocess.run(['cut', '-f', '1', 'sonataLeftSpine.semits'], stdout=sonata_left_column_semits)
			subprocess.run(['correl', '-s', '[\ \*\.r=]', '-f', 'input.semits', 'sonataLeftColumn.semits'], stdout=sonata_left_column_correl)

		bar_numbers_with_high_correlations = self.get_correlated_bar_numbers()
		bars_as_myank_strings = self.get_bars_as_myank_strings(bar_numbers_with_high_correlations)

		return bars_as_myank_strings

	def get_bars_as_myank_strings (self, bar_numbers_with_high_correlations:list):
		bars_as_myank_strings = []
		skips = 0
		for i, bar_number in enumerate(bar_numbers_with_high_correlations):
			if skips > 0:
				skips -= 1
				continue
			else:
				myank_bars = str(bar_number)
				current_bar_i = i
				while True:
					if current_bar_i < (len(bar_numbers_with_high_correlations) - 1):
						if (bar_numbers_with_high_correlations[current_bar_i+1] - bar_numbers_with_high_correlations[current_bar_i]) == 1:
							current_bar_i += 1
							skips += i
						else:
							bars_as_myank_strings.append(myank_bars if i == current_bar_i else f'{bar_number}-{bar_numbers_with_high_correlations[current_bar_i]}')
							break
					else:
						break
		return bars_as_myank_strings

	def get_correlated_bar_numbers (self):
		bar_numbers_with_high_correlations = []
		with\
			open('sonataLeftColumn.semits') as sonata_left_column_semits,\
			open('sonataLeftColumn.correl') as sonata_left_column_correl:
			semits_file = sonata_left_column_semits.readlines()
			for i, line in enumerate(sonata_left_column_correl):
				correlation:float = 0
				try:
					correlation = float(line.replace(',', '.'))
				except ValueError:
					pass
				if correlation >= Correlations_in_kern_repository.CORRELATION_MINIMUM:	# negative ?
					# append the BARNUMBER when a certain correlation is achieved
					line_index = i
					barline_found = False
					while not barline_found:
						line_index -= 1
						line_with_barline = semits_file[line_index]
						if line_with_barline.startswith('='):
							barline_found = True
							try:
								bar_number = int(line_with_barline[1:])
								bar_numbers_with_high_correlations.append(bar_number)
							except ValueError:
								pass
		return bar_numbers_with_high_correlations

	def selectPlatform (self):

		humdrum_directory:str = None
		input_file_name:str = None
		wsl:bool = None

		if platform.platform() == 'Windows-10-10.0.18363-SP0':
			humdrum_directory = '/home/bjorn/humdrum-tools'
			input_file_name = "/mnt/b/Users/Bjorn/Documents/testikel/input.txt"
			wsl = True
			os.environ['PATH'] += f':{humdrum_directory}/humdrum/bin'	# is "humdrum/bin" compulsory?
		else:
			humdrum_directory = '/usr/local/humdrum-tools/humdrum'
			input_file_name = '/Users/Arturjds/Desktop/input.krn'
			wsl = False
			os.environ['PATH'] += f':{humdrum_directory}'

		if humdrum_directory is None:
			raise Exception('Humdrum directory has not been provided.')
		elif input_file_name is None:
			raise Exception('Input file name has not been provided')
		elif wsl is None:
			raise Exception('Cannot tell if Windows Subsystem for Linux is being used.')
		else:
			return humdrum_directory, input_file_name, wsl

c = Correlations_in_kern_repository()
print(c.dict)


# every_sonata_bar_correlation = []

# for sonata_file_name in os.listdir(f"{humdrum_directory}/data/mozart/piano-sonatas/kern"):
# # if True:
# # 	sonata_file_name = 'sonata01-1.krn'
# 	with\
# 		open(os.path.join(f"{humdrum_directory}/data/mozart/piano-sonatas/kern", sonata_file_name), 'r') as file,\
# 		open('input.semits', 'w') as input_semits,\
# 		open('mozart.semits', 'w') as sonata_semits,\
# 		open('sonataLeftSpine.semits', 'w') as sonata_left_spine_semits,\
# 		open('sonataLeftColumn.semits', 'w') as sonata_left_column_semits,\
# 		open('sonataLeftColumn.correl', 'w') as sonata_left_column_correl:
		
# 		subprocess.run(['semits', '-x', input_file_name], stdout=input_semits)
# 		subprocess.run(['semits', '-x', f'{humdrum_directory}/data/mozart/piano-sonatas/kern/{sonata_file_name}'], stdout=sonata_semits)
# 		subprocess.run(['extract', '-p', '1', 'mozart.semits'], stdout=sonata_left_spine_semits)
# 		subprocess.run(['cut', '-f', '1', 'sonataLeftSpine.semits'], stdout=sonata_left_column_semits)
# 		subprocess.run(['correl', '-s', '[\ \*\.r=]', '-f', 'input.semits', 'sonataLeftColumn.semits'], stdout=sonata_left_column_correl)

# 	bar_numbers_with_high_correlations = []	# D O N E !
# 	CORRELATION_MINIMUM = 0.4
# 	with\
# 		open('sonataLeftColumn.semits') as sonata_left_column_semits,\
# 		open('sonataLeftColumn.correl') as sonata_left_column_correl:
# 		semits_file = sonata_left_column_semits.readlines()
# 		for i, line in enumerate(sonata_left_column_correl):
# 			correlation:float = 0
# 			try:
# 				correlation = float(line.replace(',', '.'))
# 			except ValueError:
# 				pass
# 			if correlation >= CORRELATION_MINIMUM:	# negative ?
# 				# append the BARNUMBER when a certain correlation is achieved
# 				line_index = i
# 				barline_found = False
# 				while not barline_found:
# 					line_index -= 1
# 					line_with_barline = semits_file[line_index]
# 					if line_with_barline.startswith('='):
# 						barline_found = True
# 						try:
# 							bar_number = int(line_with_barline[1:])
# 							bar_numbers_with_high_correlations.append(bar_number)
# 						except ValueError:
# 							pass

# 	bars_as_myank_strings = []
# 	skips = 0
# 	for i, bar_number in enumerate(bar_numbers_with_high_correlations):
# 		if skips > 0:
# 			skips -= 1
# 			continue
# 		else:
# 			myank_bars = str(bar_number)
# 			current_bar_i = i
# 			while True:
# 				if current_bar_i < (len(bar_numbers_with_high_correlations) - 1):
# 					if (bar_numbers_with_high_correlations[current_bar_i+1] - bar_numbers_with_high_correlations[current_bar_i]) == 1:
# 						current_bar_i += 1
# 						skips += i
# 					else:
# 						bars_as_myank_strings.append(myank_bars if i == current_bar_i else f'{bar_number}-{bar_numbers_with_high_correlations[current_bar_i]}')
# 						break
# 				else:
# 					break

# 	every_sonata_bar_correlation.append([sonata_file_name, bars_as_myank_strings])

# print(every_sonata_bar_correlation)

# results_as_tsv = ''
# for sonata_results in every_sonata_bar_correlation:
# 	sonata_name, correlated_bars = sonata_results
# 	results_as_tsv += sonata_name
# 	for bar in correlated_bars:
# 		results_as_tsv += '\t' + bar
# 	results_as_tsv += '\n'

# results = open('correlated_bars.txt', 'w')
# results.write(results_as_tsv)
				



#    1) for each file in mozart piano sonatas:
#        a) create files:
#            — create a file with bass called bassVoice.krn
#            – creae a file with melody called trebleVoice.krn
#            – create a file with all the middle voices called middleVoices.krn