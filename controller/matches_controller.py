from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request
from errors import errors
from view.view import View
from service.service import Service


class MatchesController(BaseController):

    def handle_get(self, request: Request) -> Response:
        matches_dto = self.service.get_all_matches_dto(request.query_params)
        print(matches_dto)
        html = self.view.render_template("matches.html", matches=matches_dto)
        return Response(html, 200)

    def handle_post(self, request: Request) -> Response:
        pass
        # match_dto = self.service.add_score(request.form_data)
        # html = self.view.render_template("match.html", match=match_dto)
        # return Response(html, 200)
