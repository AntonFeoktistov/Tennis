from enum import Enum
from typing import Optional


class Scores(Enum):
    LOVE = "0"
    FIFTEEN = "15"
    THIRTY = "30"
    FORTY = "40"
    AD = "AD"

    def next(self):
        """Возвращает следующий статус"""
        members = list(self.__class__)
        current_index = members.index(self)
        if current_index + 1 < len(members):
            return members[current_index + 1]
        return None

    def prev(self):
        """Возвращает предыдущий"""
        members = list(self.__class__)
        current_index = members.index(self)
        if current_index - 1 >= 0:
            return members[current_index - 1]
        return None
