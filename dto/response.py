class Response:
    def __init__(
        self,
        body: str,
        status: int = 200,
        content_type: str = "text/html",
        headers: list = None,
    ):
        self.body = body
        self.status = status
        self.content_type = content_type
        self.headers = headers if headers is not None else []
