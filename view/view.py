from jinja2 import Environment, FileSystemLoader
import os


class View:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_index(self, name=None):
        return self.render_template("index.html")
