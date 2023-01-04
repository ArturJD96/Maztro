# coding=utf-8
import os
import platform
import subprocess
# import asyncio

class Correlations_in_kern_repository:

	CORRELATION_MINIMUM = 0.99
	results = {} # remove it

	def __init__ (self, kern_input:str=None, kern_repository_directory:str=None):

		print(f'INPUT : {type(kern_input)}\nkern_input')

		if kern_input is not None and not isinstance(kern_input, str): raise Exception("Argument 'kern input' must be a string!")
		if kern_repository_directory is not None and not isinstance(kern_repository_directory, str): raise Exception("Argument 'kern repository directory' must be a string!")

		self.humdrum_directory, self.input_file_name, self.wsl = self.selectPlatform()
		kern_repo_dir = kern_repository_directory or f"{self.humdrum_directory}/data/mozart/piano-sonatas/test"

		self.results = {}	# dict with all the sonatas and their correlations in left-most spine.
		for i, piece in enumerate(os.listdir(kern_repo_dir)):
			correlated_bars_with_correlations = self.get_correlated_bars(f'{kern_repo_dir}/{piece}')
			print(correlated_bars_with_correlations)
			if correlated_bars_with_correlations:
				self.results[piece] = correlated_bars_with_correlations
				Correlations_in_kern_repository.results

		print("CHECKING FINISHED.")

	def report_correlation_for_piece (self, piece, results):
		print('testikel')
		print(piece, results)
		tag = f'<script type="text/x-humdrum" id=""'
		# <script type="text/x-humdrum" id="example1">
		# **kern
		# *M4/4
		# =1-
		# 4g
		# 8fL
		# 8eJ
		# 4d
		# 4c
		# =
		# *-
		# </script>

	def get_correlated_bars (self, kern_piece_dir:str):
		if not isinstance(kern_piece_dir, str): raise Exception("Argument 'kern_piece_dir' must be a string!")
		print(f'checking {kern_piece_dir}')
		self.run_query_using_cmd_and_create_files_with_results(kern_piece_dir)
		bar_numbers_with_correlations = self.get_correlated_bar_numbers()
		bars_as_myank_strings = self.get_bars_as_myank_strings(bar_numbers_with_correlations)
		return bars_as_myank_strings

	# def run_query_using_cmd_and_create_files_with_results (self, kern_piece_dir:str):

	def run_query_using_cmd_and_create_files_with_results (self, kern_piece_dir:str):
		# This version of the function uses less files
		# and concatenates the whole sonata kern file
		# into a single **kern spine.
		# ! ! ! the chord from the spine should be split
		# ! ! ! into separate spines in order for correl
		# ! ! ! to give satisfactory results.

		# kern_only_dir = '../query/pieceKernOnly.kern'
		# one_spine_dir = '../query/pieceOneSpine.kern'
		# piece_semits_dir = '../query/piece.semits'
		# input_semits_dir = '../query/input.semits'
		# piece_correl_dir = '../query/piece.correl'
		# with\
		# 	open(kern_piece_dir, 'r') as file,\
		# 	open(kern_only_dir, 'w') as piece_kern_only,\
		# 	open(one_spine_dir, 'w') as piece_one_kern_spine,\
		# 	open(piece_semits_dir, 'w') as piece_semits,\
		# 	open(input_semits_dir, 'w') as input_semits,\
		# 	open(piece_correl_dir, 'w') as piece_correl:

		# 	subprocess.run(['extract','-i','**kern',kern_piece_dir], stdout=piece_kern_only) # use only **kern spines
		# 	subprocess.run(['cleave','-d','" "','-i','**kern','-o','**kern',kern_only_dir], stdout=piece_one_kern_spine) # concatenate every **kern spines into one **kern spine containing chords only.
		# 	subprocess.run(['semits','-x',one_spine_dir], stdout=piece_semits) # turn notes into semits
		# 	subprocess.run(['semits','-x',self.input_file_name], stdout=input_semits) # make input file to semits. !!! WORTHWHILE to do this only once at the beginning.
		# 	subprocess.run(['correl','-s','[\ \*\.r=]','-f',input_semits_dir,piece_semits_dir], stdout=piece_correl)	

		#! ! ! P R E V I O U S ! ! !
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
		#! ! !                 ! ! !


	def get_bars_as_myank_strings (self, bar_numbers_with_high_correlations:list):
		bars_as_myank_strings = []
		skips = 0
		for i, bar_number_with_correlation in enumerate(bar_numbers_with_high_correlations):
			if skips > 0:
				skips -= 1
				continue
			else:
				myank_bars = str(bar_number_with_correlation)
				current_bar_i = i
				while True:
					if current_bar_i < (len(bar_numbers_with_high_correlations) - 1):
						if (bar_numbers_with_high_correlations[current_bar_i+1] - bar_numbers_with_high_correlations[current_bar_i]) == 1:
							current_bar_i += 1
							skips += i
						else:
							bar_span = myank_bars if i == current_bar_i else f'{bar_number_with_correlation}-{bar_numbers_with_high_correlations[current_bar_i]}'
							bars_as_myank_strings.append(bar_span)
							break
					else:
						break
		return bars_as_myank_strings

	def get_correlated_bar_numbers (self):
		bar_numbers_with_correlations = []
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
								bar_numbers_with_correlations.append(bar_number)
							except ValueError:
								pass
		return bar_numbers_with_correlations

	def selectPlatform (self):

		humdrum_directory:str = None
		input_file_name:str = None
		wsl:bool = None

		print(platform.platform())

		if platform.platform() == 'Windows-10-10.0.18363-SP0' or platform.platform() == 'Linux-4.4.0-18362-Microsoft-x86_64-with-Ubuntu-18.04-bionic' or platform.platform() == "Linux-4.4.0-18362-Microsoft-x86_64-with-glibc2.27":
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

#c = Correlations_in_kern_repository()
