# services/email_renderer.py
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class EmailRenderer:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), "../templates")
        self.env = Environment(loader=FileSystemLoader(template_path))
    
    def render_newsletter(self, user, articles):
        template = self.env.get_template("newsletter.html.j2")
        return template.render(
            topics=", ".join(user.preferences["topics"]),
            articles=articles,
            date=datetime.now().strftime("%B %d, %Y"),
            unsubscribe_url=f"https://yourdomain.com/unsubscribe/{user.id}"
        )