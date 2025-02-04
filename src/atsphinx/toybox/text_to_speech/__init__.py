"""Text to speech bundler."""

from typing import Optional
from uuid import UUID, uuid4

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders.dummy import DummyBuilder
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective

from .providers import load_provider


class tts(nodes.General, nodes.Element):  # noqa: D101
    pass


class TTSDirective(SphinxDirective):  # noqa: D101
    has_content = True

    def run(self):  # noqa: D102
        return [tts(text="\n".join(self.content))]


class TextToSpeechDomain(Domain):
    """Domain to manage TTS resources."""

    name = __name__
    label = "tts"

    @property
    def texts(self) -> dict[str, UUID]:
        """Cache storage for OGP metadata."""
        self.data.setdefault("texts", {})
        return self.data["texts"]

    def process_doc(
        self, env: BuildEnvironment, docname: str, document: nodes.document
    ):
        """Find TTS source."""
        for n in document.findall(tts):
            self.texts.setdefault(n["text"], uuid4())


class TTSBuilder(DummyBuilder):
    """Builder to render catalog of TTS sources."""

    name = "tts"
    epilog = "FUTURE: generate audio files from sources."

    def finish(self):  # noqa: D102
        provider = load_provider(self.config.tts_provider, self.config.tts_options)
        domain: Optional[TextToSpeechDomain] = self.env.domains.get(__name__)  # type: ignore
        if not domain:
            raise Exception("Domain is not found.")
        for text, uuid in domain.texts.items():
            outdir = self.outdir.joinpath("_static/_tts")
            outdir.mkdir(parents=True, exist_ok=True)
            filepath = outdir.joinpath(f"{uuid}.{provider.format}")
            if not filepath.exists():
                print("NEW", uuid, text)
                provider.generate_audio(text, filepath)
            else:
                print("   ", uuid, text)


def skip_it(self, node: nodes.Node):  # noqq: D104
    raise nodes.SkipNode()


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("tts_provider", "dummy", "env")
    app.add_config_value("tts_options", {}, "env")
    app.add_node(tts, html=(skip_it, None))
    app.add_directive("tts", TTSDirective)
    app.add_domain(TextToSpeechDomain)
    app.add_builder(TTSBuilder)
    return {
        "version": 0,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
