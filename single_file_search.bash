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
echo "a"
semits -x /mnt/b/Users/Bjorn/Documents/testikel/input.txt > input.semits
echo "b"
semits -x $1 > mozart.semits
echo "c"
extract -p 1 mozart.semits > sonataLeftSpine.semits
echo "d"
cut -f 1 sonataLeftSpine.semits > sonataLeftColumn.semits
echo "e"
correl -s [\ \*\.r=] -f input.semits sonataLeftColumn.semits > sonataLeftColumn.correl

cat sonataLeftColumn.correl