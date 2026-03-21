from sqlalchemy.orm import Session
from model.match import Match
from model.player import Player
from sqlalchemy import update


class MatchRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_match(self, player1: Player, player2: Player) -> Match:
        match = Match(player1_id=player1.id, player2_id=player2.id)
        self.create_score_json(match, player1, player2)
        self.session.add(match)
        self.session.flush()
        return match

    def get_match_by_id(self, match_id: int) -> Match | None:
        return self.session.get(Match, match_id)

    def get_match_by_uuid(self, match_uuid: str) -> Match | None:
        return self.session.query(Match).filter(Match.uuid == match_uuid).first()

    def get_filtred_matches(
        self,
        player_name: str = None,
        completed_only: bool = False,
        page: int = 1,
        per_page: int = 5,
    ) -> tuple[list[Match], int]:

        query = self.session.query(Match)
        if player_name and player_name.strip():
            query = query.filter(
                (Match.player1.has(Player.name.ilike(f"%{player_name}%")))
                | (Match.player2.has(Player.name.ilike(f"%{player_name}%")))
            )
        if completed_only:
            query = query.filter(Match.winner_id.isnot(None))

        total_count = query.count()
        offset = (page - 1) * per_page
        matches = query.order_by(Match.id.desc()).limit(per_page).offset(offset).all()

        return matches, total_count

    def get_all_matches(self) -> list[Match]:
        return self.session.query(Match).all()

    def update_score(self, match_id: int, new_score: dict) -> None:
        stmt = update(Match).where(Match.id == match_id).values(score=new_score)
        self.session.execute(stmt)

    def update_winner(self, match_id: int, winner_id: int) -> None:
        stmt = update(Match).where(Match.id == match_id).values(winner_id=winner_id)
        self.session.execute(stmt)

    def save(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def create_score_json(self, match: Match, player1: Player, player2: Player):
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
