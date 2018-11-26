import imitation_chess

import json
import os
import os.path

import sys
import multiprocessing

boardStates = '../data/mapping_lichess_db_standard_rated_2018-10_collected.json'

ouputDir = '../data/early_games'

num_engines = 8

mainQ = multiprocessing.Queue()

def jsonOutput(results, board):
    bestmove = str(results[0].bestmove)
    ponderedmove = str(results[0].ponder)
    return json.dumps({'bestmove' : bestmove, 'ponderedmove' : ponderedmove,
    'probs' : results[1], 'board' : board})

def EngineProcess(enginePath, boards):
    engine = imitation_chess.EngineHandler('lc0', enginePath, threads = 1)
    for b in boards:
        board = imitation_chess.fen(b)
        ret = engine.getBoardProbs(board, movetime = 10000 * 10)
        q.put(jsonOutput(ret, b))
    q.put(False)
    return


def main():

    targetNetwork = sys.argv[1]
    if not os.path.isfile(targetNetwork):
        raise RuntimeError("Invalid network path")

    outputName = os.path.join(ouputDir, os.path.basename(targetNetwork)[:-6])

    os.makedir(ouputDir, exist_ok = True)

    with open(boardStates) as f:
        boards = [json.loads(l) for l in f]

    sortedBoards = sorted(boards, key = lambda x : sum(x['counts'].values()))

    splitBoards = {i : [] for i in range(num_engines)}
    for i, b in enumerate(sortedBoards):
        splitBoards[i % num_engines].append(b['board'])

    print({k : len(v) for k, v in splitBoards.items})


if __name__ == '__main__':
    main()
