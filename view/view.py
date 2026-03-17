# view/view.py
from jinja2 import Environment, FileSystemLoader
import os


class View:
    def __init__(self):
        # Настройка Jinja2 один раз при создании View
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_template(self, template_name, **context):
        """Загружает и рендерит шаблон с переданными переменными"""
        template = self.env.get_template(template_name)
        return template.render(**context)

    def render_index(self, name=None):
        """Специализированный метод для главной страницы"""
        return self.render_template("index.html", name=name or "Гость")

    def render_error(self, message):
        """Метод для страницы ошибки"""
        return self.render_template("error.html", error=message)
