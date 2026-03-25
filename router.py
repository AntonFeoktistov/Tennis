from dto.response import Response


class Router:
    def __init__(self, container):
        self.container = container
        self.routes = {
            "/": self.container.get_index_controller,
            "/newmatch": self.container.get_new_match_controller,
            "/matches": self.container.get_matches_controller,
            "/match-score": self.container.get_match_score_controller,
        }

    def dispatch(self, request) -> Response:
        controllers_factory = self.routes.get(request.path)
        if not controllers_factory:
            return Response("Page not found", 404)

        controller = controllers_factory()

        if request.method == "GET":
            return controller.handle_get(request)
        elif request.method == "POST":
            return controller.handle_post(request)
        else:
            return Response("Method not allowed", 405)
