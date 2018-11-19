#!/bin/bash

# Add -debug to see engine output

engine1=1100
engine2=1200

weightsDir="/w/225/reidmcy/chess/imitation-chess/networks"


#No time control, but only look at 800 new nodes a round

cutechess-cli -rounds 100 -tournament gauntlet -concurrency 4 \
 -pgnout "hai-${engine1}-v-hai-${engine2}.pgn" \
 -engine name="hai-${engine1}" cmd=lc0 arg="--threads=1" arg="--noise" arg="--weights=${weightsDir}/${engine1}-64x6-140000.pb.gz" arg="--playouts=800" arg="--noponder"\
 -engine name="hai-${engine2}" cmd=lc0 arg="--threads=1" arg="--noise" arg="--weights=${weightsDir}/${engine2}-64x6-140000.pb.gz" arg="--playouts=800" arg="--noponder"\
 -each proto=uci tc=inf
