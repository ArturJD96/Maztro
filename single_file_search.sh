#!/usr/bin/env bash


#extract -i **kern $1 > query/pieceKernOnly.kern
#echo "test0"
#cleave -d " " -i '**kern' -o '**kern' query/pieceKernOnly.kern > query/pieceOneSpine.kern
#echo "test1"
#semits -x /mnt/b/Users/Bjorn/Documents/testikel/input.txt > query/input.semits # this one should run only once!
#echo "test2"
#semits -x query/pieceOneSpine.kern > query/piece.semits
#echo "test3"
#correl -s [\ \*\.r=] -f query/input.semits query/piece.semits > query/piece.correl
#echo "test4"

# echo "a"
# semits -x /mnt/b/Users/Bjorn/Documents/testikel/input.txt > input.semits
# echo "b"
# semits -x $1 > mozart.semits
# echo "c"
# extract -p 1 mozart.semits > sonataLeftSpine.semits
# echo "d"
# cut -f 1 sonataLeftSpine.semits > sonataLeftColumn.semits
# echo "e"
# correl -s [\ \*\.r=] -f input.semits sonataLeftColumn.semits > sonataLeftColumn.correl

# cat sonataLeftColumn.correl


# open('mozart_kern_only.krn', 'w') as piece_kern_only,\
# open('mozart_one_kern_spine.krn', 'w') as piece_one_kern_spine,\
# open('sonataLeftSpine.semits', 'w') as sonata_left_spine_semits,\
# open('input.semits', 'w') as input_semits,\
# open('sonataLeftColumn.correl', 'w') as sonata_left_column_correl:

# # 1) remove all spines that are not **kern
# subprocess.run(['extract','-i','**kern',kern_piece_dir], stdout=piece_kern_only)
# # 2) concatenate every **kern spines into one **kern spine (containing chords only).
# subprocess.run(['cleave','-d','" "','-i','**kern','-o','**kern','mozart_kern_only.krn'], stdout=piece_one_kern_spine)
# # 3) turn each note into semits
# subprocess.run(['semits','-x','mozart_one_kern_spine.krn'], stdout=sonata_left_spine_semits)
# # 4) make input file to semits. !!! WORTHWHILE to do this only once at the beginning.
# subprocess.run(['semits', '-x', self.input_file_name], stdout=input_semits)
# # 5) look for correlation
# subprocess.run(['correl', '-s', '[\ \*\.r=]', '-f', 'input.semits', 'sonataLeftColumn.semits'], stdout=sonata_left_column_correl)	

# 1) remove all spines that are not **kern
extract -i '**kern' $2 > ./mozart_kern_only.krn

# 2) concatenate every **kern spines into one **kern spine (containing chords only).
# cleave -d " " -i '**kern' -o '**kern' ./mozart_kern_only.krn > ./mozart_one_kern_spine.krn
# 3) turn each note into semits
# semits -x ./mozart_one_kern_spine.krn > ./sonataLeftSpine.semits

# OR (instead of 2 and 3)leave only the leftmost spine:
	semits -x $2 > ./mozart.semits
	extract -p 1 ./mozart.semits > ./sonataLeftSpine.semits
	cut -f 1 ./sonataLeftSpine.semits > ./sonataLeftColumn.semits
	#cat ./sonataLeftColumn.semits

# 4) make input file to semits. !!! WORTHWHILE to do this only once at the beginning.
semits -x $3 > ./input.semits

# 5) look for correlation
correl -s [\ \*\.r=] -f ./input.semits ./sonataLeftColumn.semits > ./sonataLeftColumn.correl
