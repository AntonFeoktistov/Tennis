from dataclasses import dataclass
from .score_dto import ScoreDto
from .player_dto import PlayerDto


@dataclass
class MatchDto:
    id: int
    uuid: str
    player1: PlayerDto
    player2: PlayerDto
    winner: PlayerDto | None
    score1: ScoreDto
    score2: ScoreDto


#   return {
#             "id": match.id,
#             "uuid": match.uuid,
#             "player1_id": match.player1_id,
#             "player2_id": match.player2_id,
#             "winner_id": match.winner_id,
#             "score1": score1,
#             "score2": score2,
#             "player1_name": match.player1.name if match.player1 else None,
#             "player2_name": match.player2.name if match.player2 else None,
#             "winner_name": winner.name if winner else None,
#         }
