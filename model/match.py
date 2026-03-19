from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from data.db import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"))
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    score = Column(JSON, default={})

    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])

    def __repr__(self):
        return f"<Match(id={self.id}, player1_id={self.player1_id}, player2_id={self.player2_id})>"

    @classmethod
    def get_by_uuid(cls, session, match_uuid):
        """Получить матч по UUID"""
        return session.query(cls).filter(cls.uuid == match_uuid).first()
