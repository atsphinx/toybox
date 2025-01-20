"""Stlite embbeding extension."""

from pathlib import Path
from typing import Any, Optional

from docutils import nodes
from docutils.parsers.rst import Directive, directives  # type:ignore
from jinja2 import Template
from sphinx.application import Sphinx
from sphinx.builders.html._assets import _CascadingStyleSheet
from sphinx.util import logging

from .. import utils

DEFAULT_STLITE_VERSION = "0.76.0"

package_root = Path(__file__).parent
logger = logging.getLogger(__name__)

view_template = Template((package_root / "view.html.jinja").read_text(encoding="utf8"))


class stlite(nodes.Element, nodes.General):  # noqa: D101
    pass


def visit_stlite(self, node: stlite):
    """Inject br tag (html only)."""
    app: Sphinx = self.builder.app
    self.body.append(
        view_template.render(node.attributes, stlite_version=app.config.stlite_version)
    )


class Stlite(Directive):  # noqa: D101
    option_spec = {
        "id": directives.unchanged,
        "requirements": directives.unchanged,
    }
    has_content = True

    def run(self):  # noqa: D102
        node = stlite()
        node.attributes = self.options
        node.attributes["requirements"] = [
            f'"{r}"' for r in self.options["requirements"].split(",")
        ]
        node.attributes["code"] = "\n".join(self.content)
        return [
            node,
        ]


def register_static_path(app, config):  # noqa: D103
    config.html_static_path.insert(0, str(package_root / "static"))


def inject_stlite_assets(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: Optional[nodes.document] = None,
):
    """Update context when document will render stlite content."""
    if not doctree:
        return
    if not list(doctree.findall(stlite)):
        return

    stlite_version = app.config.stlite_version
    context["css_files"] += [
        f"https://cdn.jsdelivr.net/npm/@stlite/browser@{stlite_version}/build/style.css",
        _CascadingStyleSheet("_static/atsphinx-stlite.css"),
    ]


def setup(app: Sphinx):  # noqa: D103
    app.add_node(stlite, html=(visit_stlite, utils.pass_node_walking))
    app.add_directive("stlite", Stlite)
    app.add_config_value("stlite_version", DEFAULT_STLITE_VERSION, "html", str)
    app.connect("config-inited", register_static_path)
    app.connect("html-page-context", inject_stlite_assets)
    return {}
