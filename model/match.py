from sqlalchemy import JSON, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player1_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.id"))
    score = Column(JSON, nullable=False, default={})
    # Отношения
    player1 = relationship(
        "Player", foreign_keys=[player1_id], back_populates="matches_as_player1"
    )
    player2 = relationship(
        "Player", foreign_keys=[player2_id], back_populates="matches_as_player2"
    )
    winner = relationship(
        "Player", foreign_keys=[winner_id], back_populates="won_matches"
    )

    def __repr__(self):
        return f"<Match(id={self.id}, player1_id={self.player1_id}, player2_id={self.player2_id}, winner_id={self.winner_id})>"

    def update_score(self, player_id: int, new_data: dict):
        """Обновляет счёт и гарантирует сохранение"""
        # Создаём копию
        score_copy = dict(self.score)

        # Обновляем
        if str(player_id) in score_copy:
            score_copy[str(player_id)].update(new_data)

        # Присваиваем (SQLAlchemy видит изменение)
        self.score = score_copy
