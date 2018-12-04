import imitation_chess

import os
import multiprocessing

nProcesses = 64
num_games = 1


resultsDir = 'all_games'

def main():

    os.makedirs(resultsDir, exist_ok=True)
    engines = imitation_chess.listAllEngines()

    opponents = []
    for i, e1 in enumerate(engines):
        for e2 in engines[i:]:
            opponents.append((e1, e2, num_games))

    with multiprocessing.Pool(processes = nProcesses) as pool:
        games = pool.starmap(imitation_chess.playTourney, opponents)
        print("Writing results")
        for (e1, e2, _), g in zip(opponents, games):
            e1Name = json.loads(e1)['name']
            e2Name = json.loads(e2)['name']
            with open(os.path.join(resultsDir, f"{e1Name}-{e2Name}.pgn"), 'a') as f:
                for game in games:
                    f.write(str(g))
                    f.write('\n')
    print("Done")

if __name__ == '__main__':
    main()
