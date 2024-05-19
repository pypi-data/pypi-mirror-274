from typing import Iterable, TextIO, Sequence
import chess.pgn

def read_pgns(pgn: TextIO) -> Iterable[chess.pgn.Game]:
  """Read all games from a PGN file"""
  while (game := chess.pgn.read_game(pgn)) is not None:
    yield game

def read_sans(game: chess.pgn.Game) -> Sequence[str]:
  """Read all moves from a game"""
  return [node.san() for node in game.mainline()]