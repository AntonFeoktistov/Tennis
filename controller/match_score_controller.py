from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request
from errors import errors
from view.view import View
from service.service import Service


class MatchScoreController(BaseController):

    def handle_get(self, request: Request) -> Response:
        match_data = self.service.get_match(request.query_params)
        print(match_data)
        print(request.query_params)
        if match_data:
            html = self.view.render_template("match.html", match=match_data)
            return Response(html, 200)
        html = self.view.render_template("not_found.html")
        return Response(html, 404)

    def handle_post(self, request: Request) -> Response:
        match_data = self.service.add_score(request.form_data)
        return Response(
            body="",
            status=302,
            headers=[("Location", f"/match-score?uuid={match_data["uuid"]}")],
        )
