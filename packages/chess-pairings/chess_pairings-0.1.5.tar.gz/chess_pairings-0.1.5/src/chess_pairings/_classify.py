from typing import Callable, Mapping, Sequence, Iterable, Literal, overload
import chess.pgn
from chess_pairings.types import GamesMapping, gameId

@overload
def classify(
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str | None] = lambda x: x.get('Event'),
  headers2group: Callable[[Mapping[str, str]], str | None],
  return_unclassified: Literal[True],
) -> tuple[GamesMapping[chess.pgn.Game], Sequence[chess.pgn.Game]]:
  ...

@overload
def classify(
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str | None] = lambda x: x.get('Event'),
  headers2group: Callable[[Mapping[str, str]], str | None],
  return_unclassified: Literal[False] = False,
) -> GamesMapping[chess.pgn.Game]:
  ...
  
def classify(
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str | None] = lambda x: x.get('Event'),
  headers2group: Callable[[Mapping[str, str]], str | None],
  return_unclassified: bool = False,
) -> tuple[GamesMapping[chess.pgn.Game], Sequence[chess.pgn.Game]] | GamesMapping[chess.pgn.Game]:    
  
  classified_games = GamesMapping[chess.pgn.Game]()
  unclassified_games = []
  
  for game in games:
    hdrs = game.headers
    tournId = headers2tournId(hdrs)
    group = headers2group(hdrs)
    rnd_brd = hdrs.get('Round', '').split('.')
    if tournId is None or group is None or len(rnd_brd) != 2:
      unclassified_games.append(game)
    else:
      round, board = rnd_brd
      classified_games[gameId(tournId, group, round, board)] = game

  if return_unclassified:
    return classified_games, unclassified_games
  else:
    return classified_games