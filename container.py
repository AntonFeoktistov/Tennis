from view.view import View
from service.service import Service
from controller.index_controller import IndexController
from controller.matches_controller import MatchesController
from controller.new_match_controller import NewMatchController
from controller.match_score_controller import MatchScoreController


class Container:
    def __init__(self):
        self.view = View()
        self.service = Service()

    def get_index_controller(self):
        return IndexController(self.view, self.service)

    def get_matches_controller(self):
        return MatchesController(self.view, self.service)

    def get_new_match_controller(self):
        return NewMatchController(self.view, self.service)

    def get_match_score_controller(self):
        return MatchScoreController(self.view, self.service)
