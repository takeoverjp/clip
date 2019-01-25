#!/bin/sh -xe

for infile in `ls -1 data/*.jpg`;
do
    outfile=${infile%.jpg}_clipped.raw
    ./clip.py $infile $outfile
done

rm -f data/hdr.mnist data/images.mnist
dd if=/dev/zero of=data/hdr.mnist count=16 bs=1
cat data/hdr.mnist data/*_clipped.raw > data/images.mnist
