from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request


class MatchScoreController(BaseController):

    def handle_get(self, request: Request) -> Response:
        match_dto = self.service.get_match(request.query_params)
        if match_dto:
            html = self.view.render_template("match.html", match=match_dto)
            return Response(html, 200)
        html = self.view.render_template("not_found.html")
        return Response(html, 404)

    def handle_post(self, request: Request) -> Response:
        match_dto = self.service.add_score(request.form_data)
        if match_dto:
            return Response(
                body="",
                status=302,
                headers=[("Location", f"/match-score?uuid={match_dto.uuid}")],
            )
        html = self.view.render_template("not_found.html")
        return Response(html, 404)
