from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request
from errors import errors
from view.view import View
from service.service import Service


class MatchesController(BaseController):

    def handle_get(self, request: Request) -> Response:
        page_data = self.service.get_all_matches_data(request.query_params)
        html = self.view.render_template("matches.html", **page_data)
        return Response(html, 200)

    def handle_post(self, request: Request) -> Response:
        match_data = self.service.add_score(request.form_data)
        html = self.view.render_template("match.html", match=match_data)
        return Response(html, 200)
