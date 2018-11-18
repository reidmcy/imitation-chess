import re
import sys
import os
import os.path


outputSuffix = '-clean'

def getNextGame(f):
    out = ''
    isBullet = False
    ncount = 0
    for l in f:
        out += l
        if l == '\n':
            ncount += 1
            if ncount > 1:
                break
        elif l.startswith('[Event '):
            if 'bullet' in l.lower():
                isBullet = True
    return out, isBullet

def cleanPGN(targetPath):
    dirname, filename = os.path.split(os.path.splitext(targetPath)[0])
    outputName = os.path.join(dirname, f"{filename}{outputSuffix}.pgn")
    with open(targetPath) as fin, open(outputName, 'w') as fout:
        game, isBul = getNextGame(fin)
        if len(game) < 1:
            break
        elif not isBul:
            fout.write(game)


def main():
    for gamesPath in sys.argv[1:]:
        cleanPGN(gamesPath)

if __name__ == '__main__':
    main()
