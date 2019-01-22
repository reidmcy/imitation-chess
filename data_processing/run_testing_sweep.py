import imitation_chess

import os
import json
import multiprocessing

nProcesses = 64

resultsDir = 'sweep_ada_2048_0'

gamesDir = '../testing_games'

def main():

    os.makedirs(resultsDir, exist_ok=True)
    engines = imitation_chess.listHaibrids(netsDir = '2048', configs = {'movetime' : 1000, 'nodes' : 0}) + imitation_chess.listLeelas(configs = {'movetime' : 1000, 'nodes' : 0})

    engines = sorted(engines)

    targets = []

    for e in os.scandir(gamesDir):
        for e1 in engines:
            targets.append((e1, e.path, resultsDir))

    print("Starting run")
    with multiprocessing.Pool(processes = nProcesses) as pool:
        results = pool.starmap(imitation_chess.checkTrajectories, targets)
    print("Done")

if __name__ == '__main__':
    main()
