from typing import Dict, Optional
from model.match import Match
from model.player import Player


from typing import Dict, Optional
from model.match import Match
from model.player import Player


class ScoreMixin:

    def update_score_dict(
        self, score_dict: dict, player_id: int, opponent_id: int
    ) -> dict:
        """Обновляет словарь со счетом и возвращает новый словарь"""
        import copy

        new_score = copy.deepcopy(score_dict)

        player_score = new_score[str(player_id)]
        opponent_score = new_score[str(opponent_id)]

        # Проверяем, не закончился ли уже матч
        if player_score.get("sets", 0) == 2 or opponent_score.get("sets", 0) == 2:
            print("Match already finished")
            return new_score

        # Логика подсчета очков
        if self._is_game_ball(player_score, opponent_score):
            self._add_game(player_score, opponent_score)
        elif self._is_tiebreak(player_score, opponent_score):
            player_score["points"] += 1
            # Проверяем победу в тай-брейке
            if self._is_tiebreak_won(player_score, opponent_score):
                self._add_game(player_score, opponent_score)
        elif player_score.get("points") == 40:
            if opponent_score.get("points") == 40:
                player_score["points"] = "AD"
            elif opponent_score.get("points") == "AD":
                opponent_score["points"] = 40
            else:
                # Выигрыш гейма
                player_score["points"] = "GAME"
                self._add_game(player_score, opponent_score)
        else:
            current = player_score.get("points")
            if current in (0, 15):
                player_score["points"] = current + 15
            elif current == 30:
                player_score["points"] = 40

        return new_score

    def _add_game(self, player_score: Dict, opponent_score: Dict) -> None:
        """Увеличивает счет по геймам"""
        player_score["games"] += 1
        player_score["points"] = 0
        opponent_score["points"] = 0

        # Проверяем, выигран ли сет
        if self._is_set_won(player_score, opponent_score):
            self._add_set(player_score, opponent_score)

    def _add_set(self, player_score: Dict, opponent_score: Dict) -> None:
        """Увеличивает счет по сетам"""
        player_score["sets"] += 1
        player_score["games"] = 0
        opponent_score["games"] = 0
        player_score["points"] = 0
        opponent_score["points"] = 0

    def _is_game_ball(self, player_score: Dict, opponent_score: Dict) -> bool:
        """Проверяет, есть ли у игрока гейм-бол"""
        player_points = player_score.get("points")
        opponent_points = opponent_score.get("points")

        # В тай-брейке
        if self._is_tiebreak(player_score, opponent_score):
            return player_points >= 6 and player_points - opponent_points >= 1

        # В обычном гейме
        if player_points == "AD":
            return True
        if player_points == 40 and opponent_points not in (40, "AD"):
            return True
        return False

    def _is_set_won(self, player_score: Dict, opponent_score: Dict) -> bool:
        """Проверяет, выигран ли сет"""
        player_games = player_score.get("games", 0)
        opponent_games = opponent_score.get("games", 0)

        # Сет выигран при разнице в 2 гейма и минимум 6 геймах
        # или при счете 7:5, 7:6 и т.д.
        if player_games >= 6 and player_games - opponent_games >= 2:
            return True
        if player_games == 7 and opponent_games in (5, 6):
            return True
        return False

    def _is_tiebreak(self, player_score: Dict, opponent_score: Dict) -> bool:
        """Проверяет, идет ли тай-брейк"""
        player_games = player_score.get("games", 0)
        opponent_games = opponent_score.get("games", 0)
        return player_games == 6 and opponent_games == 6

    def _is_tiebreak_won(self, player_score: Dict, opponent_score: Dict) -> bool:
        """Проверяет, выигран ли тай-брейк"""
        player_points = player_score.get("points", 0)
        opponent_points = opponent_score.get("points", 0)

        # Тай-брейк выигран при минимум 7 очках и разнице в 2 очка
        return player_points >= 7 and player_points - opponent_points >= 2

    def get_winner_from_score(self, score_dict: dict, match: Match) -> Optional[Player]:
        """Определяет победителя по словарю счета"""
        p1_score = score_dict.get(str(match.player1_id), {})
        p2_score = score_dict.get(str(match.player2_id), {})

        if p1_score.get("sets", 0) == 2:
            return match.player1
        if p2_score.get("sets", 0) == 2:
            return match.player2
        return None
