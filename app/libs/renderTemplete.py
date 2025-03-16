from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import os

# Cấu hình Jinja2
template_env = Environment(
    loader=FileSystemLoader(os.path.join(
        os.path.join(Path(__file__).resolve().parent.parent, "templates")
    )),
)

# Hàm render template


def render_template(template_name: str, **context):
    template = template_env.get_template(template_name)
    return template.render(**context)
