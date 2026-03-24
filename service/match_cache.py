from model.match import Match


class MatchCache:

    def __init__(self):
        self._matches = {}

    def get(self, uuid: str):
        return self._matches.get(uuid)

    def set(self, match: Match) -> None:
        self._matches[match.uuid] = match

    def remove(self, uuid: str) -> None:
        if uuid in self._matches:
            del self._matches[uuid]

    def get_all(self) -> list[Match]:
        return list(self._matches.values())

    def count(self) -> int:
        return len(self._matches)

    def clear(self) -> None:
        self._matches.clear()
