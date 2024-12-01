"""Stlite embbeding extension."""

from pathlib import Path
from typing import Any, Optional

from docutils import nodes
from docutils.parsers.rst import Directive, directives  # type:ignore
from jinja2 import Template
from sphinx.application import Sphinx
from sphinx.util import logging

from .. import utils

STLITE_VERSION = "0.73.0"

package_root = Path(__file__).parent
logger = logging.getLogger(__name__)

page_template = Template((package_root / "page.html.jinja").read_text(encoding="utf8"))
view_template = Template((package_root / "view.html.jinja").read_text(encoding="utf8"))


class stlite(nodes.Element, nodes.General):  # noqa: D101
    pass


def visit_stlite(self, node: stlite):
    """Inject br tag (html only)."""
    app: Sphinx = self.builder.app
    widget_uri = f"_widgets/{node['id']}"
    out = app.outdir / widget_uri / "index.html"
    docname = app.env.path2doc(node.document["source"])
    if docname is None:
        logger.warning("It failed to resolve docname of document.")
        return
    widget_url = app.builder.get_relative_uri(docname, widget_uri)
    out.parent.mkdir(exist_ok=True, parents=True)
    out.write_text(page_template.render(node.attributes), encoding="utf8")
    self.body.append(view_template.render(node.attributes, url=widget_url))


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
    if not doctree.findall(stlite):
        return

    context["script_files"].append(
        f"https://cdn.jsdelivr.net/npm/@stlite/mountable@{STLITE_VERSION}/build/stlite.js"
    )
    context["css_files"].append(
        f"https://cdn.jsdelivr.net/npm/@stlite/mountable@{STLITE_VERSION}/build/stlite.css"
    )


def setup(app: Sphinx):  # noqa: D103
    app.add_node(stlite, html=(visit_stlite, utils.pass_node_walking))
    app.add_directive("stlite", Stlite)
    app.connect("html-page-context", inject_stlite_assets)
    return {}
