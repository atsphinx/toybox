import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Type


@dataclass
class Options:
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


def load_provider(name: str, config: dict) -> Provider:
    """Resolve and load provider object."""
    module_name = f"{__name__}.{name}"
    provider_class = f"{name.title()}Provider"
    options_class = f"{name.title()}Options"
    module = importlib.import_module(module_name)
    provider: Type[Provider] = getattr(module, provider_class)
    options: Options = getattr(module, options_class)(**config)
    return provider(options=options)
