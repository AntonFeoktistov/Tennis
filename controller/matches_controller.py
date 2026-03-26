from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request


class MatchesController(BaseController):

    def handle_get(self, request: Request) -> Response:
        matches_dto = self.service.get_all_matches_dto(request.query_params)
        if matches_dto:
            html = self.view.render_template("matches.html", matches=matches_dto)
            return Response(html, 200)
        html = self.view.render_template("not_found.html")
        return Response(html, 404)

    def handle_post(self, request: Request) -> Response:
        pass
