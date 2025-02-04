import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TypedDict


class Options(TypedDict):
    """Base class of options."""

    pass


@dataclass
class Engine:
    """Generator for audio file called by builder."""

    format: ClassVar[str]
    """Format(extension) of generated files."""
    options: Options
    """Engine options."""

    def generate_audio(self, text: str, out: Path, extra: dict = {}):
        """Generate audio file."""
        raise NotImplementedError


def load_engine(name: str, options: Options) -> Engine:
    """Resolve and load engine object."""
    module_name = f"{__name__}.{name}"
    class_name = f"{name.title()}Engine"
    module = importlib.import_module(module_name)
    klass = getattr(module, class_name)
    return klass(options=options)
