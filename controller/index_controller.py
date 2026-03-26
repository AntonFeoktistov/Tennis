from controller.base_controller import BaseController
from dto.response import Response


class IndexController(BaseController):

    def handle_get(self, request) -> Response:
        html = self.view.render_index()
        return Response(html, 200)

    def handle_post(self, request) -> Response:
        pass
