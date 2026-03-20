from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from data.db import Base
import uuid


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    uuid = Column(
        String, unique=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"))
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    score = Column(JSON, default={})

    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])
