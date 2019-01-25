#!/bin/sh -xe

for infile in `ls -1 data/*.jpg`;
do
    outfile=${infile%.jpg}_clipped.raw
    ./clip.py $infile $outfile
done
