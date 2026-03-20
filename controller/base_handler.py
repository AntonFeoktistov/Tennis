from functools import cached_property
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os
import urllib
import model

from view.view import View
from service.service import Service
from errors.errors import *
from repository.player_repository import *


class BaseHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            html = self.view.render_index(name="Пользователь")
            self.send_html(html, 200)
        elif self.path == "/newmatch":
            html = self.view.render_template("new_match.html")
            self.send_html(html, 200)
        elif self.path == "/matches":
            matches = self.service.get_all_matches_data()
            html = self.view.render_template("matches.html", matches=matches)
            self.send_html(html, 200)

        elif self.path.startswith("/match-score"):
            query = self.get_query_params()
            match_data = self.service.get_match(query)
            if match_data:
                html = self.view.render_template("match.html", match=match_data)
                self.send_html(html, 200)
                return
            html = self.view.render_template("not_found.html")
            self.send_html(html, 404)
        elif self.path.startswith("/static/"):
            self.send_static()
        else:
            html = self.view.render_template("not_found.html")
            self.send_html(html, 404)

    def do_POST(self):
        form = self.get_form()
        if self.path == "/newmatch":
            try:
                match_data = self.service.create_match(form)
                html = self.view.render_template("match.html", match=match_data)
                self.send_html(html, 200)
            except NotValidNameError as e:
                html = self.view.render_template("new_match.html", error=True)
                self.send_html(html, 400)
        if self.path == "/match-score":
            match_data = self.service.add_score(form)
            html = self.view.render_template("match.html", match=match_data)
            self.send_html(html, 200)

    def send_html(self, html: str, status: int):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def send_static(self):
        file_path = self.path[len("/static/") :]
        try:
            with open(os.path.join("static", file_path), "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            html = self.view.render_error("Файл не найден")
            self.send_html(html, 404)

    def get_form(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            return urllib.parse.parse_qs(post_data.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def get_query_params(self):
        parsed = urllib.parse.urlparse(self.path)
        return urllib.parse.parse_qs(parsed.query)

    @cached_property
    def view(self):
        return View()

    @cached_property
    def service(self):
        return Service()
