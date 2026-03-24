from dataclasses import dataclass

import pytest
from service.service import ScoreMixin
from model.match import Match
from model.player import Player

"""нужно сделать параметризацию чтобы вводить 3 числа: сеты геймыы и поинты """


@dataclass
class Score:
    score_dict: dict
    player_id: int
    opponent_id: int


class TestScoreMixin:
    @pytest.fixture
    def scorer(self, scope="class"):
        return ScoreMixin()

    @pytest.fixture
    def score(self, scope="session"):
        player_id = 1
        opponent_id = 2
        score_dict = {
            "1": {"sets": 0, "games": 0, "points": 0},
            "2": {"sets": 0, "games": 0, "points": 0},
        }
        return Score(score_dict, player_id, opponent_id)

    def set_score(self, score: dict, sets=0, games=0, points=0):
        score["sets"] = sets
        score["games"] = games
        score["points"] = points

    @pytest.mark.parametrize("points, points_after", [(0, 15), (15, 30), (30, 40)])
    def test_add_points_not_tiebreak_not_gameball(
        self, scorer, score: Score, points, points_after
    ):
        player_score = score.score_dict[score.player_id]
        opponent_score = score.score_dict[score.opponent_id]
        self.set_score(
            player_score,
        )
        scorer.update_score_dict(score.score_dict, score.player_id, score.oponent_id)

        assert player["points"] == player_after["points"]
