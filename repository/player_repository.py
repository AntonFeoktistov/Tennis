from model.player import Player
from sqlalchemy.orm import Session


class PlayerRepository:
    """Класс для работы с игроками в БД"""

    def __init__(self, session: Session):
        self.session = session

    def get_player_by_id(self, player_id: int) -> Player | None:
        """Найти игрока по ID"""
        return self.session.get(Player, player_id)

    def get_player_by_name(self, name: str) -> Player | None:
        """Найти игрока по имени"""
        return self.session.query(Player).filter(Player.name == name).first()

    def get_or_create_player(self, name: str) -> Player:
        """Найти игрока или создать нового"""
        player = self.get_player_by_name(name)
        if not player:
            player = Player(name=name)
            self.session.add(player)
            self.session.flush()  # получаем ID без commit
        return player

    def create_player(self, name: str) -> Player:
        """Создать нового игрока"""
        player = Player(name=name)
        self.session.add(player)
        self.session.flush()
        return player

    def exists(self, name: str) -> bool:
        """Проверить, существует ли игрок"""
        return (
            self.session.query(Player).filter(Player.name == name).first() is not None
        )

    def get_all(self) -> list[Player]:
        """Получить всех игроков"""
        return self.session.query(Player).all()
