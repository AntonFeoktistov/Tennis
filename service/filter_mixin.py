from typing import List
from model.match import Match
from dto.match_dto import MatchDto


class FilterMixin:

    def _parse_filters(self, query: dict):
        filter_name = (query.get("filter_name") or [""])[0]
        completed_only = (query.get("completed_only") or [""])[0]
        page = (query.get("page") or [1])[0]
        current_page = int(page) if str(page).isdigit() else 1
        return filter_name, completed_only, current_page

    def _filter_by_completed_only(self, completed_only, match_repo, cache):
        if completed_only:
            return match_repo.get_completed_matches()
        else:
            completed = match_repo.get_completed_matches()
            active = cache.get_all()

            all_matches = completed + active
            unique = []
            seen_ids = set()

            for match in all_matches:
                if match.id not in seen_ids:
                    seen_ids.add(match.id)
                    unique.append(match)

            return unique

    def _filter_by_player_name(
        self, matches: List[Match], filter_name: str
    ) -> List[Match]:
        if filter_name:
            filtered_matches = []
            for match in matches:
                player1_name = match.player1.name.lower() if match.player1 else ""
                player2_name = match.player2.name.lower() if match.player2 else ""
                if (
                    filter_name.lower() in player1_name
                    or filter_name.lower() in player2_name
                ):
                    filtered_matches.append(match)
            return filtered_matches
        return matches

    def _sort_matches(self, matches: List[Match]) -> List[Match]:
        matches.sort(key=lambda m: m.id, reverse=True)
        return matches

    def _paginate_matches(self, matches: List[Match], page: int, per_page: int = 5):

        start = (page - 1) * per_page
        end = start + per_page
        return matches[start:end]
