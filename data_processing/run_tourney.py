import imitation_chess

import os
import json
import multiprocessing

nProcesses = 86
num_games = 10
num_leelas = 12

resultsDir = 'hairbrid_new_games_ada'

def main():

    os.makedirs(resultsDir, exist_ok=True)

    engines = imitation_chess.listLeelas(configs = {'movetime' : 10000, 'nodes' : 10000})

    engines += imitation_chess.listStockfishs() + imitation_chess.listRandoms()

    engines += imitation_chess.listHaibrids(configs = {'movetime' : 10000, 'nodes' : 10000}, suffix = '.pb.gz')

    engines = sorted(engines)

    opponents = []
    for i, e1 in enumerate(engines):
        if 'hiabrid' in e1 and ('1200_1500' in e1 or '2000_2300' in e1):
            lcount = 0
            for e2 in engines[i:]:
                dat = json.loads(e2)
                if 'leela' in e1:
                    lcount += 1
                    if lcount >= num_leelas:
                        continue
                opponents.append((e1, e2, num_games, resultsDir))

    #stockfish takes a while at high skill
    #opponents = opponents[::-1]

    for i in range(100):
        with multiprocessing.Pool(processes = nProcesses) as pool:
            games = pool.starmap(imitation_chess.playTourney, opponents*1000)
            print("Done circuit")
    print("Done")

if __name__ == '__main__':
    main()
