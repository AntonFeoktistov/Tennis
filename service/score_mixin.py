import copy
from dto.score_dto import ScoreDto


class ScoreMixin:

    def update_score_dict(
        self, score_dict: dict, player_id: int, opponent_id: int
    ) -> dict:

        new_score = copy.deepcopy(score_dict)

        player_score = ScoreDto.from_dict(new_score[str(player_id)])
        opponent_score = ScoreDto.from_dict(new_score[str(opponent_id)])

        if self._is_game_ball(player_score, opponent_score):
            self._add_game(player_score, opponent_score)
        elif self._is_tiebreak(player_score, opponent_score):
            player_score.points += 1
        else:
            self._add_points(player_score, opponent_score)

        new_score[str(player_id)] = player_score.to_dict()
        new_score[str(opponent_id)] = opponent_score.to_dict()
        return new_score

    def _add_points(self, player_score: ScoreDto, opponent_score: ScoreDto):
        if player_score.points == 40:
            if opponent_score.points == 40:
                player_score.points = "AD"
            elif opponent_score.points == "AD":
                opponent_score.points = 40
        else:
            current_points = player_score.points
            if current_points in (0, 15):
                player_score.points += 15
            elif current_points == 30:
                player_score.points += 10

    def _add_game(self, player_score: ScoreDto, opponent_score: ScoreDto) -> None:
        if self._is_set_ball(player_score, opponent_score):
            self._add_set(player_score, opponent_score)
        else:
            player_score.games += 1
            player_score.points = opponent_score.points = 0

    def _add_set(self, player_score: ScoreDto, opponent_score: ScoreDto) -> None:
        player_score.sets += 1
        player_score.games = opponent_score.games = 0
        player_score.points = opponent_score.points = 0

    def _is_game_ball(self, player_score: ScoreDto, opponent_score: ScoreDto) -> bool:
        if self._is_tiebreak(player_score, opponent_score):
            return (
                player_score.points >= 6
                and player_score.points - opponent_score.points >= 1
            )
        if player_score.points == "AD":
            return True
        if player_score.points == 40 and opponent_score.points not in (40, "AD"):
            return True
        return False

    def _is_set_ball(self, player_score: ScoreDto, opponent_score: ScoreDto) -> bool:
        if player_score.games >= 5 and player_score.games - opponent_score.games >= 1:
            return True
        if player_score.games == opponent_score.games == 6:
            if self._is_game_ball(player_score, opponent_score):
                return True
        return False

    def _is_tiebreak(self, player_score: ScoreDto, opponent_score: ScoreDto) -> bool:
        return player_score.games == 6 and opponent_score.games == 6

    # def update_score_dict(
    #     self, score_dict: dict, player_id: int, opponent_id: int
    # ) -> dict:

    #     new_score = copy.deepcopy(score_dict)
    #     player_score = new_score[str(player_id)]
    #     opponent_score = new_score[str(opponent_id)]

    #     if self._is_game_ball(player_score, opponent_score):
    #         self._add_game(player_score, opponent_score)
    #     elif self._is_tiebreak(player_score, opponent_score):
    #         player_score["points"] += 1
    #     else:
    #         self._add_points(player_score, opponent_score)

    #     return new_score

    # def _add_points(self, player_score: dict, opponent_score: dict):
    #     if player_score.get("points") == 40:
    #         if opponent_score.get("points") == 40:
    #             player_score["points"] = "AD"
    #         elif opponent_score.get("points") == "AD":
    #             opponent_score["points"] = 40
    #     else:
    #         current_points = player_score.get("points")
    #         if current_points in (0, 15):
    #             player_score["points"] += 15
    #         elif current_points == 30:
    #             player_score["points"] += 10

    # def _add_game(self, player_score: Dict, opponent_score: Dict) -> None:
    #     if self._is_set_ball(player_score, opponent_score):
    #         self._add_set(player_score, opponent_score)
    #     else:
    #         player_score["games"] += 1
    #         player_score["points"] = 0
    #         opponent_score["points"] = 0

    # def _add_set(self, player_score: Dict, opponent_score: Dict) -> None:
    #     player_score["sets"] += 1
    #     player_score["games"] = 0
    #     opponent_score["games"] = 0
    #     player_score["points"] = 0
    #     opponent_score["points"] = 0

    # def _is_game_ball(self, player_score: Dict, opponent_score: Dict) -> bool:
    #     player_points = player_score.get("points")
    #     opponent_points = opponent_score.get("points")

    #     if self._is_tiebreak(player_score, opponent_score):
    #         return player_points >= 6 and player_points - opponent_points >= 1

    #     if player_points == "AD":
    #         return True
    #     if player_points == 40 and opponent_points not in (40, "AD"):
    #         return True
    #     return False

    # def _is_set_ball(self, player_score: Dict, opponent_score: Dict) -> bool:
    #     player_games = player_score.get("games", 0)
    #     opponent_games = opponent_score.get("games", 0)

    #     if player_games >= 5 and player_games - opponent_games >= 1:
    #         return True
    #     if player_games == opponent_games == 6:
    #         if self._is_game_ball(player_score, opponent_score):
    #             return True
    #     return False

    # def _is_tiebreak(self, player_score: Dict, opponent_score: Dict) -> bool:
    #     player_games = player_score.get("games", 0)
    #     opponent_games = opponent_score.get("games", 0)
    #     return player_games == 6 and opponent_games == 6

    # def get_winner(self, match: Match) -> Optional[Player]:
    #     p1_score = match.score.get(str(match.player1_id), {})
    #     p2_score = match.score.get(str(match.player2_id), {})

    #     if p1_score.get("sets", 0) == 2:
    #         return match.player1
    #     if p2_score.get("sets", 0) == 2:
    #         return match.player2
    #     return None
