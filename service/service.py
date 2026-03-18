import copy
from functools import cached_property

from .validator import Validator
from errors import errors
from repository.player_repository import PlayerRepository
from repository.match_repository import MatchRepository
from model.player import Player
from model.match import Match
from data.db import get_session
from .scores_enum import Scores


class Service:
    def __init__(self):
        self.session = get_session()
        self.player_repository = PlayerRepository(self.session)
        self.match_repository = MatchRepository(self.session)

    def create_match(self, form: dict):
        name1 = (form.get("player1") or [""])[0]
        name2 = (form.get("player2") or [""])[0]
        error1 = not self.validator.is_name_valid(name1)
        error2 = not self.validator.is_name_valid(name2)
        if error1 or error2:
            raise errors.NotValidNameError(error1, error2)
        player1 = self.player_repository.get_or_create_player(name1)
        player2 = self.player_repository.get_or_create_player(name2)
        match = self.match_repository.create_match(player1, player2)
        self.match_repository.save()
        return (match, player1, player2)

    def add_score(self, form: dict):
        match_id = form.get("match_id")[0]
        match = self.match_repository.get_match_by_id(match_id)
        player_id = form.get("player_id")[0]
        opponent_id = self.get_opponent_id(match, player_id)
        player = self.player_repository.get_player_by_id(player_id)
        opponent = self.player_repository.get_player_by_id(opponent_id)

        match = self.add_point(match, player_id, opponent_id)
        print(match.score[str(player.id)])
        print(match.score[str(opponent.id)])
        winner = self.get_winner(match)
        match.winner_id = winner.id if winner else None
        match = self.match = self.match_repository.get_match_by_id(match_id)
        return (match, player, opponent)

    def add_point(self, match: Match, player_id: int, opponent_id: int):
        player_score = match.score.get(str(player_id))
        opponent_score = match.score.get(str(opponent_id))

        if self.is_game_ball(player_score, opponent_score):
            self.add_game(player_score, opponent_score)
        elif self.is_tiebreak(player_score, opponent_score):
            player_score["points"] += 1
        elif player_score.get("points") == 40:
            if opponent_score.get("points") == 40:
                player_score["points"] = "AD"
            elif opponent_score.get("points") == "AD":
                opponent_score["points"] = 40
        else:
            player_score["points"] += 15

        score_copy = copy.deepcopy(match.score)
        score_copy[str(player_id)] = player_score
        score_copy[str(opponent_id)] = opponent_score
        match.score = score_copy
        return match

    def add_game(self, player_score, opponent_score):
        if not self.is_set_ball(player_score, opponent_score):
            player_score["games"] += 1
            player_score["points"] = 0
            opponent_score["points"] = 0
            return
        self.add_set(player_score, opponent_score)

    def add_set(self, player_score, opponent_score):
        if not self.is_set_ball(player_score, opponent_score):
            player_score["sets"] += 1
            player_score["points"] = 0
            opponent_score["points"] = 0
            player_score["games"] = 0
            opponent_score["games"] = 0

    def get_winner(
        self,
        match: Match,
    ):
        if match.score[str(match.player1_id)].get("sets") == 2:
            return match.player1
        if match.score[str(match.player2_id)].get("sets") == 2:
            return match.player2
        return None

    def is_game_ball(self, player_score, opponent_score):
        if player_score.get("points") == 40:
            if opponent_score.get("points") not in (40, "AD"):
                return True
        if player_score.get("points") == "AD":
            if opponent_score.get("points") != "AD":
                return True
        if player_score.get("points") == 6:
            return True

        return False

    def is_set_ball(self, player_score, opponent_score):
        if player_score.get("games") >= 5:
            if player_score.get("games") - opponent_score("games") >= 2:
                return True
        return False

    def is_match_ball(self, player_score, opponent_score):
        if player_score.get("sets") == 1:
            return True
        return False

    def is_tiebreak(self, player_score, opponent_score):
        return player_score.get("games") == 6 and (opponent_score.get("games") == 6)

    def get_all_matches(self):
        pass

    def get_opponent_id(self, match: Match, player_id: int):
        if match.player1_id == player_id:
            return match.player2_id
        return match.player1_id

    @cached_property
    def validator(self):
        return Validator()
