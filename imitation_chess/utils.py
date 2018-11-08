import chess

fenComps = 'rrqn2k1/8/pPp4p/2Pp1pp1/3Pp3/4P1P1/R2NB1PP/1Q4K1 w KQkq - 0 1'.split()

def fen(s):
    splitS = s.split()
    return chess.Board(' '.join(splitS + fenComps[len(splitS):]))
