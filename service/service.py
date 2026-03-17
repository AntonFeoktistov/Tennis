from functools import cached_property

from .validator import Validator
from errors import errors
from repository.player_repository import PlayerRepository
from repository.match_repository import MatchRepository
from data.db import get_session


class Service:
    def __init__(self):
        self.session = get_session()
        self.player_repo = PlayerRepository(self.session)
        self.match_repo = MatchRepository(self.session)

    def make_match(self, form: dict):
        player_1 = (form.get("player_1") or [""])[0]
        player_2 = (form.get("player_2") or [""])[0]
        error_1 = self.validator.validate_name(player_1)
        error_2 = self.validator.validate_name(player_2)
        if error_1 or error_2:
            raise errors.NotValidNameError(error_1, error_2)

    def get_all_matches(self):
        pass

    @cached_property
    def validator(self):
        return Validator
