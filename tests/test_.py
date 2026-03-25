import pytest
from service.service import ScoreMixin


class TestScoreMixin:

    @pytest.fixture(scope="class")
    def scorer(self):
        return ScoreMixin()

    @pytest.mark.parametrize("points, points_after", [(0, 15), (15, 30), (30, 40)])
    def test_update_score_dict_0_15_30(self, points, points_after, scorer):
        score_dict = {
            "1": {"sets": 0, "games": 0, "points": points},
            "2": {"sets": 0, "games": 0, "points": 0},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)
        assert result["1"]["points"] == points_after
        assert result["2"]["points"] == 0

    @pytest.mark.parametrize(
        "opponent_points, points_after, opponent_after",
        [(40, "AD", 40), ("AD", 40, 40)],
    )
    def test_update_score_dict_40_not_wingame(
        self, scorer, opponent_points, points_after, opponent_after
    ):
        score_dict = {
            "1": {"sets": 0, "games": 0, "points": 40},
            "2": {"sets": 0, "games": 0, "points": opponent_points},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["points"] == points_after
        assert result["2"]["points"] == opponent_after

    @pytest.mark.parametrize("points, opponent_points", [(40, 30), ("AD", 40)])
    def test_update_score_dict_win_game(self, scorer, points, opponent_points):
        score_dict = {
            "1": {"sets": 0, "games": 0, "points": points},
            "2": {"sets": 0, "games": 0, "points": opponent_points},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["games"] == 1
        assert result["2"]["games"] == 0
        assert result["1"]["points"] == 0
        assert result["2"]["points"] == 0

    @pytest.mark.parametrize("games, opponent_games", [(5, 5), (5, 6)])
    def test_update_score_dict_win_game_5_not_winset(
        self, scorer, games, opponent_games
    ):
        score_dict = {
            "1": {"sets": 0, "games": games, "points": 40},
            "2": {"sets": 0, "games": opponent_games, "points": 30},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["sets"] == 0
        assert result["2"]["sets"] == 0
        assert result["1"]["games"] == games + 1
        assert result["2"]["games"] == opponent_games
        assert result["1"]["points"] == 0
        assert result["2"]["points"] == 0

    @pytest.mark.parametrize("games, opponent_games", [(6, 4), (6, 5)])
    def test_update_score_dict_win_set(self, scorer, games, opponent_games):
        score_dict = {
            "1": {"sets": 0, "games": games, "points": 40},
            "2": {"sets": 0, "games": opponent_games, "points": 30},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["sets"] == 1
        assert result["1"]["games"] == 0
        assert result["2"]["games"] == 0
        assert result["1"]["points"] == 0
        assert result["2"]["points"] == 0

    def test_update_score_start_tiebreak(self, scorer):
        score_dict = {
            "1": {"sets": 0, "games": 6, "points": 0},
            "2": {"sets": 0, "games": 6, "points": 0},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["sets"] == 0
        assert result["1"]["games"] == 6
        assert result["2"]["games"] == 6
        assert result["1"]["points"] == 1
        assert result["2"]["points"] == 0

    @pytest.mark.parametrize("points, opponent_points", [(6, 5), (6, 6)])
    def test_update_score_win_tiebreak(self, scorer, points, opponent_points):
        score_dict = {
            "1": {"sets": 0, "games": 6, "points": points},
            "2": {"sets": 0, "games": 6, "points": opponent_points},
        }
        result = scorer.update_score_dict(score_dict, player_id=1, opponent_id=2)

        assert result["1"]["sets"] == 1
        assert result["1"]["games"] == 0
        assert result["2"]["games"] == 0
        assert result["1"]["points"] == 0
        assert result["2"]["points"] == 0
