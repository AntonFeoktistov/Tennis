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
        print(player1, player2)
        return self.match_repository.create_match(player1, player2)

    def change_score(self, form):
        player_name = form.get("player_name")
        match_id = form.get("match_id")
        player = self.player_repository.get_player_by_name(player_name)
        match = self.match_repository.get_match_by_id(match_id)
        opponent = self.match_repository.get_opponent(match, player)
        self.add_point(match, player, opponent)

    def add_point(self, match: Match, player: Player, opponent: Player):
        player_score = match.score.get(player.name)
        opponent_score = match.score.get(opponent.name)

        if player_score.get("points") in (Scores.LOVE, Scores.FIFTEEN, Scores.THIRTY):
            player_score["points"] = player.score.get("points").next()
            return

        if self.is_game_ball(player_score, opponent_score):
            self.add_game(player_score, opponent_score)
            return

        if player_score.get("points") in (0, 1, 2, 3, 4, 5):
            player_score["points"] += 1

    def add_game(self, player_score, opponent_score):
        if not self.is_set_ball(player_score, opponent_score):
            player_score["games"] += 1
            player_score["points"] = Scores.LOVE
            opponent_score["points"] = Scores.LOVE
            return
        self.add_set(player_score, opponent_score)

    def add_set(self, player_score, opponent_score):
        if not self.is_set_ball(player_score, opponent_score):
            player_score["sets"] += 1
            player_score["points"] = Scores.LOVE
            opponent_score["points"] = Scores.LOVE
            player_score["games"] = 0
            opponent_score["games"] = 0

        self.finish_match()

    def finish_match():
        pass

    def is_game_ball(self, player_score, opponent_score):
        if player_score.get("points") == Scores.FORTY:
            if opponent_score.get("points") not in (Scores.FORTY, Scores.AD):
                return True
        if player_score.get("points") == Scores.AD:
            if opponent_score.get("points") != Scores.AD:
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

    def get_all_matches(self):
        pass

    @cached_property
    def validator(self):
        return Validator()
