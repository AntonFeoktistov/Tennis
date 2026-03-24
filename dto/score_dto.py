from dataclasses import dataclass


@dataclass
class ScoreDto:
    sets: int
    games: int
    points: int | str

    def to_dict(self) -> dict:
        return {"sets": self.sets, "games": self.games, "points": self.points}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            sets=data.get("sets", 0),
            games=data.get("games", 0),
            points=data.get("points", 0),
        )
