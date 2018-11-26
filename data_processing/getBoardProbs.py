import imitation_chess

import json
import os
import os.path

import sys
import multiprocessing

boardStates = '../data/mapping_lichess_db_standard_rated_2018-10_collected.json'

ouputDir = '../data/early_games'

num_engines = 8

def jsonOutput(results, board):
    bestmove = str(results[0].bestmove)
    ponderedmove = str(results[0].ponder)
    return json.dumps({'bestmove' : bestmove, 'ponderedmove' : ponderedmove,
    'probs' : results[1], 'board' : board})

def EngineProcess(enginePath, boards, Q):
    engine = imitation_chess.EngineHandler('lc0', enginePath, threads = 1)
    for b in boards:
        board = imitation_chess.fen(b)
        ret = engine.getBoardProbs(board, movetime = 10000 * 10)
        Q.put(jsonOutput(ret, b))
    Q.put(False)
    return


def main():


    targetNetwork = sys.argv[1]
    if not os.path.isfile(targetNetwork):
        raise RuntimeError("Invalid network path")


    outputName = os.path.join(ouputDir, os.path.basename(targetNetwork)[:-6])

    print(f"Starting on: {targetNetwork} to {outputName}")

    os.makedirs(ouputDir, exist_ok = True)

    with open(boardStates) as f:
        boards = [json.loads(l) for l in f]

    sortedBoards = sorted(boards, key = lambda x : sum(x['counts'].values()))

    print(f"Loaded and sorted {len(sortedBoards)} board states")

    splitBoards = {i : [] for i in range(num_engines)}
    for i, b in enumerate(sortedBoards):
        splitBoards[i % num_engines].append(b['board'])

    print("Split into:", {k : len(v) for k, v in splitBoards.items()})

    processes = []
    mainQ = multiprocessing.Queue()

    for i in range(num_engines):
        print("Starting process: ", i)
        p = multiprocessing.Process(target=EngineProcess, args=(targetNetwork, splitBoards[i], mainQ))
        p.start()
        processes.append(p)

    print("Starting main loop")
    num_done_procs = 0
    num_done_boards = 0
    while True:
        val = mainQ.get()

        if val:
            num_done_boards += 1
            with open(outputName, 'a') as f:
                f.write(val)
                f.write('\n')
            print(f"Done {num_done_boards} boards", end ='\r')
        else:
            num_done_procs += 1
            print(f"\nProcess {num_done_procs} of {num_engines} complete")
            if num_done_procs == num_engines:
                break
    print("\nAll done, joining")
    for p in property:
        p.join()
    print("Done")



if __name__ == '__main__':
    main()
