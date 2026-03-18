# repositories/match_repository.py
from sqlalchemy.orm import Session
from model.match import Match
from model.player import Player
from datetime import datetime
from service.scores_enum import Scores


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

    def set_winner(self, match_id: int, winner_id: int) -> Match | None:
        """Установить победителя матча"""
        match = self.get_match_by_id(match_id)
        if match:
            match.winner_id = winner_id
            self.session.flush()
        return match

    def create_score_json(self, match: Match, player1: Player, player2: Player):
        match.score = {
            player1.name: {"sets": 0, "games": 0, "points": Scores.LOVE},
            player2.name: {"sets": 0, "games": 0, "points": Scores.LOVE},
        }

    def get_opponent(self, match: Match, player: Player):
        return match.player1 if match.player1 != player else match.player2
