"""GLiCID Jinja templates module."""
from pathlib import Path

from jinja2 import Environment, PackageLoader, Template, select_autoescape

TEMPLATES = Environment(
    loader=PackageLoader('glicid_spawner'),
    autoescape=select_autoescape(),
)


def get_template(name: str) -> Template:
    """Get Jinja2 template."""
    return TEMPLATES.get_template(name)


def get_template_src(name: str) -> str:
    """Get Jinja2 template source."""
    template = get_template(name)
    return Path(template.filename).read_text()


def render_template(name: str, **kwargs) -> str:
    """Render Jinja2 template."""
    return get_template(name).render(**kwargs)
