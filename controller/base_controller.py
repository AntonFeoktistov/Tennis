from dto.response import Response
from view.view import View
from service.service import Service


class BaseController:
    def __init__(self, view: View, service: Service):
        self.view = view
        self.service = service

    def handle_get(self, request) -> Response:
        return Response("Method not allowed", 405)

    def handle_post(self, request) -> Response:
        return Response("Method not allowed", 405)
