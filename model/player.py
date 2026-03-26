from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(35), nullable=False)

    matches_as_player1 = relationship(
        "Match", foreign_keys="[Match.player1_id]", back_populates="player1"
    )
    matches_as_player2 = relationship(
        "Match", foreign_keys="[Match.player2_id]", back_populates="player2"
    )
    won_matches = relationship(
        "Match", foreign_keys="[Match.winner_id]", back_populates="winner"
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}')>"
