from dataclasses import dataclass


@dataclass
class ScoreDto:
    sets: int
    games: int
    points: int | str
