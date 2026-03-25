from controller.base_controller import BaseController
from dto.response import Response
from dto.request import Request
from errors import errors


class NewMatchController(BaseController):

    def handle_get(self, request: Request) -> Response:
        html = self.view.render_template("new_match.html")
        return Response(html, 200)

    def handle_post(self, request: Request) -> Response:
        try:
            match_dto = self.service.create_match(request.form_data)
            return Response(
                body="",
                status=302,
                headers=[("Location", f"/match-score?uuid={match_dto.uuid}")],
            )
        except errors.NotValidNameError as e:
            html = self.view.render_template("new_match.html", error=True)
            return Response(html, 400)
