from model.match import Match
from model.player import Player
from .score_mixin import ScoreMixin
from .validator import Validator
from repository.player_repository import PlayerRepository
from repository.match_repository import MatchRepository
from errors import errors
from data.db import get_session
from sqlalchemy import update
from dto.player_dto import PlayerDto
from dto.match_dto import MatchDto
from dto.score_dto import ScoreDto
from dto.matches_dto import MatchesDto
from .match_cache import MatchCache
from .filter_mixin import FilterMixin


class Service(ScoreMixin, FilterMixin):
    def __init__(self):
        self.validator = Validator()
        self.player_repository = PlayerRepository
        self.match_repository = MatchRepository
        self.cache = MatchCache()

    def load_unfinished_matches(self):
        session = get_session()
        try:
            match_repo = self.match_repository(session)
            matches = match_repo.get_unfinished_matches()
            for match in matches:
                self.cache.set(match)
        finally:
            session.close()

    def save_active_matches(self):
        session = get_session()
        try:
            match_repo = self.match_repository(session)
            matches = self.cache.get_all()
            if not matches:
                return
            for match in matches:
                session.query(Match).filter(Match.id == match.id).update(
                    {"score": match.score, "winner_id": match.winner_id}
                )
            session.commit()
        except Exception as e:
            print(f"[SAVE] Ошибка: {e}")
            session.rollback()
        finally:
            session.close()
        self.cache.clear()

    def create_match(self, form: dict):
        session = get_session()
        try:
            player_repo = self.player_repository(session)
            match_repo = self.match_repository(session)

            name1 = (form.get("player1") or [""])[0]
            name2 = (form.get("player2") or [""])[0]

            if (
                not self.validator.is_name_valid(name1)
                or not self.validator.is_name_valid(name2)
                or name1 == name2
            ):
                raise errors.NotValidNameError()

            player1 = player_repo.get_or_create_player(name1)
            player2 = player_repo.get_or_create_player(name2)
            match = match_repo.create_match(player1, player2)

            match_repo.save()
            self.cache.set(match)
            match_dto = self.make_match_dto(match, None)
            return match_dto
        finally:
            session.close()

    def add_score(self, form: dict):
        session = get_session()
        try:
            match_repo = self.match_repository(session)

            match_uuid = form.get("match_uuid")[0]
            player_id = int(form.get("player_id")[0])
            match = self.cache.get(match_uuid)
            if not match:
                match = match_repo.get_match_by_uuid(match_uuid)
            opponent_id = self.get_opponent_id(match, player_id)

            new_score = self.update_score_dict(match.score, player_id, opponent_id)
            match.score = new_score
            winner = self.get_winner(match)
            if winner:
                match.winner_id = winner.id
                match_repo.update_score(match.id, new_score)
                match_repo.update_winner(match.id, winner.id)
                match_repo.save()

                self.cache.remove(match_uuid)

            return self.make_match_dto(match, winner)
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

            match = self.cache.get(uuid)
            if not match:
                match = match_repo.get_match_by_uuid(uuid)

            winner = self.get_winner(match)
            return self.make_match_dto(match, winner)
        finally:
            session.close()

    def get_opponent_id(self, match: Match, player_id: int) -> int:
        if match.player1_id == player_id:
            return match.player2_id
        elif match.player2_id == player_id:
            return match.player1_id

    def get_winner(self, match: Match):
        p1_score = match.score.get(str(match.player1_id), {})
        p2_score = match.score.get(str(match.player2_id), {})

        if p1_score.get("sets", 0) == 2:
            return match.player1
        if p2_score.get("sets", 0) == 2:
            return match.player2
        return None

    def get_all_matches_dto(self, query):
        session = get_session()
        try:
            match_repo = self.match_repository(session)

            filter_name, completed_only, current_page = self._parse_filters(query)

            matches = self._filter_by_completed_only(
                completed_only, match_repo, self.cache
            )
            matches = self._filter_by_player_name(matches, filter_name)
            matches = self._sort_matches(matches)

            total_count = len(matches)
            matches = self._paginate_matches(matches, current_page)

            matches_dto = self.make_matches_dto(
                matches, total_count, current_page, filter_name, completed_only
            )
            return matches_dto
        finally:
            session.close()

    def make_match_dto(self, match: Match, winner: Player):
        score1 = match.score.get(str(match.player1_id), {})
        score2 = match.score.get(str(match.player2_id), {})
        player1_dto = PlayerDto(id=match.player1_id, name=match.player1.name)
        player2_dto = PlayerDto(id=match.player2_id, name=match.player2.name)
        winner_dto = PlayerDto(id=winner.id, name=winner.name) if winner else None
        score1_dto = ScoreDto(score1["sets"], score1["games"], score1["points"])
        score2_dto = ScoreDto(score2["sets"], score2["games"], score2["points"])

        return MatchDto(
            match.id,
            match.uuid,
            player1_dto,
            player2_dto,
            winner_dto,
            score1_dto,
            score2_dto,
        )

    def make_matches_dto(
        self, matches: Match, total_count, current_page, filter_name, completed_only
    ):
        per_page = 5
        total_pages = (total_count + per_page - 1) // per_page
        paginated_matches = []
        for match in matches:
            winner = self.get_winner(match)
            paginated_matches.append(self.make_match_dto(match, winner))
        return MatchesDto(
            paginated_matches,
            total_count,
            total_pages,
            current_page,
            per_page,
            filter_name,
            completed_only,
        )


# match.id = match.id
#         return {
#             "id": match.id,
#             "uuid": match.uuid,
#             "player1_id": match.player1_id,
#             "player2_id": match.player2_id,
#             "winner_id": match.winner_id,
#             "score1": score1,
#             "score2": score2,
#             "player1_name": match.player1.name if match.player1 else None,
#             "player2_name": match.player2.name if match.player2 else None,
#             "winner_name": winner.name if winner else None,
#         }
