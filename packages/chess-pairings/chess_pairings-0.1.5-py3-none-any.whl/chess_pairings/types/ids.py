from typing_extensions import TypedDict

class GroupId(TypedDict):
  tournId: str
  group: str

class RoundId(GroupId):
  round: str

class GameId(RoundId):
  board: str

def gameId(tournId: str, group: str, round: str, board: str) -> GameId:
  return GameId(tournId=tournId, group=group, round=round, board=board)

def roundId(tournId: str, group: str, round: str) -> RoundId:
  return RoundId(tournId=tournId, group=group, round=round)

def groupId(tournId: str, group: str) -> GroupId:
  return GroupId(tournId=tournId, group=group)
