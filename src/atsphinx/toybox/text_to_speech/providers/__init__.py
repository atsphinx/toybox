import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TypedDict


class Options(TypedDict):
    """Base class of options."""

    pass


@dataclass
class Provider:
    """Generator for audio file called by builder."""

    format: ClassVar[str]
    """Format(extension) of generated files."""
    options: Options
    """Provider options."""

    def __post_init__(self):  # noqa: D105
        self.load()

    def load(self):
        """Load object after bind as dataclass."""
        raise NotImplementedError

    def generate_audio(self, text: str, out: Path, extra: dict = {}):
        """Generate audio file."""
        raise NotImplementedError


def load_provider(name: str, options: Options) -> Provider:
    """Resolve and load provider object."""
    module_name = f"{__name__}.{name}"
    class_name = f"{name.title()}Provider"
    module = importlib.import_module(module_name)
    klass = getattr(module, class_name)
    return klass(options=options)
