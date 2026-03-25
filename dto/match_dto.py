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
