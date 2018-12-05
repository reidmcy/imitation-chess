import imitation_chess

import os
import json
import multiprocessing

nProcesses = 48
num_games = 10


resultsDir = 'all_games_ada'

def main():

    os.makedirs(resultsDir, exist_ok=True)
    engines = imitation_chess.listAllEngines(leelaConfig={'movetime' : 1000, 'nodes' : 1000}, hiabridConfig = {'movetime' : 1000, 'nodes' : 1000})

    opponents = []
    for i, e1 in enumerate(engines):
        for e2 in engines[i:]:
            opponents.append((e1, e2, num_games, resultsDir))

    #stockfish takes a while at high skill
    #opponents = opponents[::-1]

    for i in range(1000):
        with multiprocessing.Pool(processes = nProcesses) as pool:
            games = pool.starmap(imitation_chess.playTourney, opponents)
            print("Done circuit")
    print("Done")

if __name__ == '__main__':
    main()
