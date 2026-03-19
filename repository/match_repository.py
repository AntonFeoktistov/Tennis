from sqlalchemy.orm import Session
from model.match import Match
from model.player import Player


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_match(self, player1: Player, player2: Player) -> Match:
        """Создать новый матч"""
        match = Match(player1_id=player1.id, player2_id=player2.id)
        self.create_score_json(match, player1, player2)
        self.session.add(match)
        self.session.flush()
        return match

    def get_match_by_id(self, match_id: int) -> Match | None:
        """Найти матч по ID"""
        return self.session.get(Match, match_id)

    def get_active_matches(self) -> list[Match]:
        """Получить все активные матчи"""
        return self.session.query(Match).filter(Match.winner_id == None).all()

    def get_all_matches(self) -> list[Match]:
        """Получить все матчи"""
        return self.session.query(Match).all()

    def save(self):
        """Фиксирует все изменения в БД"""
        self.session.commit()

    def rollback(self):
        """Откатывает изменения"""
        self.session.rollback()

    def create_score_json(self, match: Match, player1: Player, player2: Player):
        """Создает начальный JSON со счетом"""
        match.score = {
            str(player1.id): {
                "name": player1.name,
                "sets": 0,
                "games": 0,
                "points": 0,
            },
            str(player2.id): {
                "name": player2.name,
                "sets": 0,
                "games": 0,
                "points": 0,
            },
        }
