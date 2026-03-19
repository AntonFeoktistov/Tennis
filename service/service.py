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

            match_id = int(form.get("match_id")[0])
            player_id = int(form.get("player_id")[0])

            # Получаем матч
            match = match_repo.get_match_by_id(match_id)
            if not match:
                raise ValueError(f"Match {match_id} not found")

            opponent_id = self.get_opponent_id(match, player_id)

            print(f"BEFORE - Score from DB: {match.score}")

            # Обновляем счет через mixin
            new_score = self.update_score_dict(match.score, player_id, opponent_id)
            print(f"New score calculated: {new_score}")

            # Определяем победителя
            winner = self.get_winner_from_score(new_score, match)

            # Обновляем через прямой SQL запрос
            from model.match import Match as MatchModel

            # Обновляем счет
            stmt = (
                update(MatchModel)
                .where(MatchModel.id == match_id)
                .values(score=new_score)
            )
            session.execute(stmt)

            # Если есть победитель, обновляем и его
            if winner:
                stmt = (
                    update(MatchModel)
                    .where(MatchModel.id == match_id)
                    .values(winner_id=winner.id)
                )
                session.execute(stmt)

            # Коммитим изменения
            session.commit()
            print("Changes committed successfully")

            # Получаем обновленный матч
            session.expire_all()
            updated_match = match_repo.get_match_by_id(match_id)
            print(f"AFTER save - Score from DB: {updated_match.score}")

            match_data = self.make_match_data(updated_match, winner)
            return match_data

        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def get_opponent_id(self, match: Match, player_id: int) -> int:
        if match.player1_id == player_id:
            return match.player2_id
        elif match.player2_id == player_id:
            return match.player1_id
        raise ValueError(f"Игрок {player_id} не участвует в матче {match.id}")

    def get_all_matches(self):
        session = get_session()
        try:
            match_repo = self.match_repository(session)
            return match_repo.get_all_matches()
        finally:
            session.close()

    def make_match_data(self, match: Match, winner: Player):
        score1 = match.score.get(str(match.player1_id), {})
        score2 = match.score.get(str(match.player2_id), {})
        return {
            "id": match.id,
            "player1_id": match.player1_id,
            "player2_id": match.player2_id,
            "winner_id": match.winner_id,
            "score1": score1,
            "score2": score2,
            "player1_name": match.player1.name if match.player1 else None,
            "player2_name": match.player2.name if match.player2 else None,
            "winner_name": winner.name if winner else None,
        }
