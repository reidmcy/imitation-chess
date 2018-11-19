#!/bin/bash

# Add -debug to see engine output

engine1="${1}" #lc0
engine2="${2}" #stockfish

weightsDir="/w/225/reidmcy/chess/imitation-chess/networks"


#No time control, but only look at 800 new nodes a round

cutechess-cli -rounds 100 -tournament gauntlet -concurrency 4 \
 -pgnout "hai-${engine1}-v-stockfish-${engine2}.pgn" \
 -engine name="hai-${engine1}" cmd=lc0 arg="--threads=1" arg="--noise" arg="--weights=${weightsDir}/${engine1}-64x6-140000.pb.gz" arg="--no-ponder"\
 -engine name="stockfish-${engine2}" cmd=stockfish initstr="setoption name Ponder value False\nsetoption name Ponder value False\nsetoption name Skill Level value ${engine2}"\
 -each proto=uci tc=40/40
