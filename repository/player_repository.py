from model.player import Player
from sqlalchemy.orm import Session


class PlayerRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_player_by_id(self, player_id: int) -> Player | None:
        return self.session.get(Player, player_id)

    def get_player_by_name(self, name: str) -> Player | None:
        return self.session.query(Player).filter(Player.name == name).first()

    def get_or_create_player(self, name: str) -> Player:
        player = self.get_player_by_name(name)
        if not player:
            player = Player(name=name)
            self.session.add(player)
            self.session.flush()
        return player

    def create_player(self, name: str) -> Player:
        player = Player(name=name)
        self.session.add(player)
        self.session.flush()
        return player

    def exists(self, name: str) -> bool:
        return (
            self.session.query(Player).filter(Player.name == name).first() is not None
        )

    def get_all(self) -> list[Player]:
        return self.session.query(Player).all()
