# repositories/match_repository.py
from functools import cached_property

from sqlalchemy.orm import Session
from model.match import Match
from model.player import Player
from datetime import datetime
from service.scores_enum import Scores
from .player_repository import PlayerRepository


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_match(self, player1: Player, player2: Player) -> Match:
        """Создать новый матч"""
        match = Match(player1_id=player1.id, player2_id=player2.id)
        self.create_score_json(match)
        self.session.add(match)
        self.session.flush()
        return match

    def get_match_by_id(self, match_id: int) -> Match | None:
        """Найти матч по ID"""
        return self.session.get(Match, match_id)

    def get_active_matches(self) -> list[Match]:
        """Получить все активные матчи"""
        return self.session.query(Match).filter(Match.winner_id == None).all()

    def save(self):
        """Фиксирует все изменения в БД"""
        self.session.commit()

    def rollback(self):
        """Откатывает изменения"""
        self.session.rollback()

    def set_winner(self, match_id: int, winner_id: int) -> Match | None:
        """Установить победителя матча"""
        match = self.get_match_by_id(match_id)
        if match:
            match.winner_id = winner_id
            self.session.flush()
        return match

    def create_score_json(self, match: Match):
        match.score = {
            match.player1_id: {"sets": 0, "games": 0, "points": 0},
            match.player2_id: {"sets": 0, "games": 0, "points": 0},
        }
