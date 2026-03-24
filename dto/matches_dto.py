from dataclasses import dataclass
from .match_dto import MatchDto


@dataclass
class MatchesDto:
    matches: list[MatchDto]
    total_count: int
    total_pages: int
    current_page: int
    per_page: int
    filter_name: str | None
    completed_only: bool | None
