import subprocess

# with\
# 	open(kern_piece_dir, 'r') as file,\
# 	open('input.semits', 'w') as input_semits,\
# 	open('mozart.semits', 'w') as sonata_semits,\
# 	open('sonataLeftSpine.semits', 'w') as sonata_left_spine_semits,\
# 	open('sonataLeftColumn.semits', 'w') as sonata_left_column_semits,\
# 	open('sonataLeftColumn.correl', 'w') as sonata_left_column_correl:
# 	subprocess.run(['semits', '-x', self.input_file_name], stdout=input_semits)
# 	subprocess.run(['semits', '-x', kern_piece_dir], stdout=sonata_semits)
# 	subprocess.run(['extract', '-p', '1', 'mozart.semits'], stdout=sonata_left_spine_semits)
# 	subprocess.run(['cut', '-f', '1', 'sonataLeftSpine.semits'], stdout=sonata_left_column_semits)
# 	subprocess.run(['correl', '-s', '[\ \*\.r=]', '-f', 'input.semits', 'sonataLeftColumn.semits'], stdout=sonata_left_column_correl)		
# #! ! !                 ! ! !

c = ['fluidsynth', '/Users/Arturjds/Desktop/STUDIA/Media\ Technology/Human\ Computer\ Interaction/assignment/app/FluidR3_GM/FluidR3_GM.sf2'] 

with open('shell_write', 'w') as file_write:
	subprocess.run(c, stdout=file_write)
	subprocess.run(c, stdout=file_write)