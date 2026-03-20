from model.match import Match
from model.player import Player
from .score_mixin import ScoreMixin
from .validator import Validator
from repository.player_repository import PlayerRepository
from repository.match_repository import MatchRepository
from errors import errors
from data.db import get_session
from sqlalchemy import update


class Service(ScoreMixin):
    def __init__(self):
        self.validator = Validator()
        self.player_repository = PlayerRepository
        self.match_repository = MatchRepository

    def create_match(self, form: dict):
        session = get_session()
        try:
            player_repo = self.player_repository(session)
            match_repo = self.match_repository(session)

            name1 = (form.get("player1") or [""])[0]
            name2 = (form.get("player2") or [""])[0]

            if not self.validator.is_name_valid(
                name1
            ) or not self.validator.is_name_valid(name2):
                raise errors.NotValidNameError()

            player1 = player_repo.get_or_create_player(name1)
            player2 = player_repo.get_or_create_player(name2)
            match = match_repo.create_match(player1, player2)

            match_repo.save()
            match_data = self.make_match_data(match, None)
            return match_data
        finally:
            session.close()

    def add_score(self, form: dict):
        session = get_session()
        try:
            match_repo = self.match_repository(session)

            match_uuid = form.get("match_uuid")[0]
            player_id = int(form.get("player_id")[0])
            match = match_repo.get_match_by_uuid(match_uuid)
            opponent_id = self.get_opponent_id(match, player_id)

            new_score = self.update_score_dict(match.score, player_id, opponent_id)
            match_repo.update_score(match.id, new_score)
            winner = self.get_winner(match)
            if winner:
                match_repo.update_winner(match.id, winner.id)

            match_repo.save()
            session.expire_all()
            updated_match = match_repo.get_match_by_id(match.id)
            return self.make_match_data(updated_match, winner)
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_match(self, query):
        session = get_session()
        try:
            match_repo = self.match_repository(session)
            uuid = (query.get("uuid") or [""])[0]
            if not uuid:
                return {}
            match = match_repo.get_match_by_uuid(uuid)
            match_data = self.make_match_data(match, match.winner) if match else {}
            return match_data
        finally:
            session.close()

    def get_opponent_id(self, match: Match, player_id: int) -> int:
        if match.player1_id == player_id:
            return match.player2_id
        elif match.player2_id == player_id:
            return match.player1_id

    def get_all_matches_data(self):
        session = get_session()
        try:
            match_repo = self.match_repository(session)
            matches = match_repo.get_all_matches()
            matches_data = []
            for match in matches:
                winner = self.get_winner(match)
                match_data = self.make_match_data(match, winner)
                matches_data.append(match_data)
            return matches_data
        finally:
            session.close()

    def make_match_data(self, match: Match, winner: Player):
        score1 = match.score.get(str(match.player1_id), {})
        score2 = match.score.get(str(match.player2_id), {})
        return {
            "id": match.id,
            "uuid": match.uuid,
            "player1_id": match.player1_id,
            "player2_id": match.player2_id,
            "winner_id": match.winner_id,
            "score1": score1,
            "score2": score2,
            "player1_name": match.player1.name if match.player1 else None,
            "player2_name": match.player2.name if match.player2 else None,
            "winner_name": winner.name if winner else None,
        }
