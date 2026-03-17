# repositories/match_repository.py
from sqlalchemy.orm import Session
from model.match import Match
from model.player import Player
from datetime import datetime


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, player1_id: int, player2_id: int) -> Match:
        """Создать новый матч"""
        match = Match(
            player1_id=player1_id, player2_id=player2_id, started_at=datetime.now()
        )
        self.session.add(match)
        self.session.flush()
        return match

    def get_by_id(self, match_id: int) -> Match | None:
        """Найти матч по ID"""
        return self.session.get(Match, match_id)

    def get_active_matches(self) -> list[Match]:
        """Получить все активные матчи"""
        return self.session.query(Match).filter(Match.winner_id == None).all()

    def set_winner(self, match_id: int, winner_id: int) -> Match | None:
        """Установить победителя матча"""
        match = self.get_by_id(match_id)
        if match:
            match.winner_id = winner_id
            match.ended_at = datetime.now()
            self.session.flush()
        return match
