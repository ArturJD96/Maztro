# coding=utf-8
import os
import platform
import subprocess

wsl = False
humdrum_directory = None
input_file_name:str = None

if platform.platform() == 'Windows-10-10.0.18363-SP0':
	humdrum_directory = '/home/bjorn/humdrum-tools'
	os.environ['PATH'] += f':{humdrum_directory}/humdrum/bin'	# is "humdrum/bin" compulsory?
	input_file_name = "/mnt/b/Users/Bjorn/Documents/testikel/input.txt"
	wsl = True
else:
	humdrum_directory = '/usr/local/humdrum-tools/humdrum'
	os.environ['PATH'] += f':{humdrum_directory}'
	input_file_name = '/Users/Arturjds/Desktop/input.krn'

every_sonata_bar_correlation = []

for sonata_file_name in os.listdir(f"{humdrum_directory}/data/mozart/piano-sonatas/kern"):
# if True:
# 	sonata_file_name = 'sonata01-1.krn'
	with\
		open(os.path.join(f"{humdrum_directory}/data/mozart/piano-sonatas/kern", sonata_file_name), 'r') as file,\
		open('input.semits', 'w') as input_semits,\
		open('mozart.semits', 'w') as sonata_semits,\
		open('sonataLeftSpine.semits', 'w') as sonata_left_spine_semits,\
		open('sonataLeftColumn.semits', 'w') as sonata_left_column_semits,\
		open('sonataLeftColumn.correl', 'w') as sonata_left_column_correl:
		
		subprocess.run(['semits', '-x', input_file_name], stdout=input_semits)
		subprocess.run(['semits', '-x', f'{humdrum_directory}/data/mozart/piano-sonatas/kern/{sonata_file_name}'], stdout=sonata_semits)
		subprocess.run(['extract', '-p', '1', 'mozart.semits'], stdout=sonata_left_spine_semits)
		subprocess.run(['cut', '-f', '1', 'sonataLeftSpine.semits'], stdout=sonata_left_column_semits)
		subprocess.run(['correl', '-s', '[\ \*\.r=]', '-f', 'input.semits', 'sonataLeftColumn.semits'], stdout=sonata_left_column_correl)

	bar_numbers_with_high_correlations = []	# D O N E !
	CORRELATION_MINIMUM = 0.4
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
			if correlation >= CORRELATION_MINIMUM:	# negative ?
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

	every_sonata_bar_correlation.append([sonata_file_name, bars_as_myank_strings])

print(every_sonata_bar_correlation)

results_as_tsv = ''
for sonata_results in every_sonata_bar_correlation:
	sonata_name, correlated_bars = sonata_results
	results_as_tsv += sonata_name
	for bar in correlated_bars:
		results_as_tsv += '\t' + bar
	results_as_tsv += '\n'

results = open('correlated_bars.txt', 'w')
results.write(results_as_tsv)
				

	
	# THEN: check, in which bar there is a linenumber
	# THEN: myank

#    1) for each file in mozart piano sonatas:
#        a) create files:
#            — create a file with bass called bassVoice.krn
#            – creae a file with melody called trebleVoice.krn
#            – create a file with all the middle voices called middleVoices.krn

# #semits -x file.kern > queried.semits

# #pseudo code
# #kernfile = 'sumname.kern'
# #subprocess.run('semits', '-x', kernfile, '>', 'queried.semits')

# #BASH
# for f in ./data/mozart/*;
#   do [extract first spine (just to test)] (something like `extract -p 1 f > /tmp/f.spine`)
#     correl -s ^= -f queried.semits /tmp/f.spine