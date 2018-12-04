import chess
import chess.uci
import chess.pgn

import pytz

import os
import os.path
import datetime

tz = pytz.timezone('Canada/Eastern')

_stockfishPath = 'stockfish'
_lc0Path = 'lc0'

_movetime = 10

networksDir = '/u/reidmcy/w/chess/imitation-chess/networks'

stockfish_SKILL = [0, 3, 6, 10, 14, 16, 18, 20]
stockfish_MOVETIMES = [50, 100, 150, 200, 300, 400, 500, 1000]
stockfish_DEPTHS = [1, 1, 2, 3, 5, 8, 13, 22]


class TourneyEngine(object):
    def __init__(self, engine, name, movetime = None, nodes = None, depth = None):
        self.engine = engine
        self.name = f"{type(self).__name__} {name}"
        self.movetime = movetime
        self.depth = depth
        self.nodes = nodes

    def __repr__(self):
        return f"<{self.name}>"

    def newgame(self):
        self.engine.ucinewgame()

    def getMove(self, board):
        self.engine.position(board)
        moves = self.engine.go(movetime = self.movetime, nodes = self.nodes, depth = self.depth)
        return moves.bestmove

    def __del__(self):
        self.engine.quit()

class StockfishEngine(TourneyEngine):
    def __init__(self, skill = 20, movetime = _movetime, depth = 30, sfPath = _stockfishPath):
        self.skill = skill

        self.stockfishPath = sfPath

        engine = chess.uci.popen_engine([self.stockfishPath])

        engine.setoption({'skill' : skill, 'Ponder' : 'false', 'UCI_AnalyseMode' : 'false'})

        super().__init__(engine, f's{skill} d{depth} {movetime}', movetime = movetime, depth = depth)

class LC0Engine(TourneyEngine):
    def __init__(self, weightsPath, nodes = None, movetime = _movetime, isHai = True, lc0Path = _lc0Path):
        self.weightsPath = weightsPath
        self.lc0Path = lc0Path
        self.isHai = isHai
        engine = chess.uci.popen_engine([self.lc0Path, f'--weights={weightsPath}'])

        super().__init__(engine, f"{os.path.basename(self.weightsPath)[:-6]} {movetime}", movetime = movetime, nodes = nodes)

class HaibridEngine(LC0Engine):
    def __init__(self, weightsPath, **kwargs):
        super().__init__(weightsPath, **kwargs, isHai = True)

class LeelaEngine(LC0Engine):
    def __init__(self, weightsPath, **kwargs):
        super().__init__(weightsPath, **kwargs, isHai = False)

def playGame(E1, E2, round = None):

    timeStarted = datetime.datetime.now(tz)
    board = chess.Board()

    E1.newgame()
    E2.newgame()

    players = [E1, E2]
    i = 0
    while not board.is_game_over():
        E = players[i % 2]
        board.push(E.getMove(board))
        i += 1
    pgnGame = chess.pgn.Game.from_board(board)

    pgnGame.headers['Event'] = f"{E1.name} vs {E1.name}"
    pgnGame.headers['White'] = E1.name
    pgnGame.headers['Black'] = E2.name
    pgnGame.headers['Date'] = timeStarted.strftime("%Y-%m-%d %H:%M:%S")
    if round is not None:
        pgnGame.headers['Round'] = round
    return pgnGame

def playTourney(E1, E2, num_rounds, event = '', progress = False):
    players = [E1, E2]
    games = []
    for i in range(num_rounds):
        if progress:
            print(f"Starting round {i} {players[0].name} vs {players[1].name}", end = '\r', flush = True)
        pgnGame = playGame(*players, round = i + 1)
        games.append(pgnGame)
        players = players[::-1]
    print("Done {num_rounds} games of {players[0].name} vs {players[1].name}")

    return games

def listLeelas():
    vals = []
    for e in os.scandir(os.path.join(networksDir, 'leela_weights')):
        if e.name.endswith('pb.gz'):
            vals.append(e.path)
    return vals

def listHaibrids():
    vals = []
    for e in os.scandir(os.path.join(networksDir)):
        if e.name.endswith('-64x6-140000.pb.gz'):
            vals.append(e.path)
    return vals

def listStockfishs():
    vals = []
    for s, m, d in zip(stockfish_SKILL, stockfish_MOVETIMES, stockfish_DEPTHS):
        vals.append({
            'skill' : s,
            'movetime' : m,
            'depth' : d,
        })
    return vals
