from http.server import BaseHTTPRequestHandler
import os
import urllib
from dto.request import Request
from dto.response import Response

router = None


class BaseHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/static/"):
            self.send_static()
            return

        request = self._create_request()
        response = router.dispatch(request)
        self._send_response(response)

    def do_POST(self):
        request = self._create_request()
        response = router.dispatch(request)
        self._send_response(response)

    def _create_request(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = parsed.path

        query = self._get_query_params()
        form = self._get_form() if self.command == "POST" else {}
        return Request(
            path=clean_path, method=self.command, query_params=query, form_data=form
        )

    def _send_response(self, response: Response):
        self.send_response(response.status)
        for header, value in response.headers:
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.body.encode())

    def _get_form(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            return urllib.parse.parse_qs(post_data.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def _get_query_params(self):
        parsed = urllib.parse.urlparse(self.path)
        return urllib.parse.parse_qs(parsed.query)

    def send_static(self):
        file_path = self.path[len("/static/") :]
        try:
            with open(os.path.join("static", file_path), "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            response = Response("File not found", 404)
            self._send_response(response)
