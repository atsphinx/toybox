"""Autoloader for pyproject.toml property."""

import inspect
from pathlib import Path
from typing import Optional

import tomli


def find_pyoroject(conf_py: Path) -> Optional[Path]:  # noqa: D103
    for d in conf_py.parents:
        pyproject_toml = d / "pyproject.toml"
        if pyproject_toml.exists():
            return pyproject_toml
        if (d / ".git").exists():
            break
    return None


def load():
    """Load configuration values from pyproect.toml."""
    caller = inspect.stack()[1]
    conf_py = Path(caller.filename)
    pyproject_toml = find_pyoroject(conf_py)
    if pyproject_toml is None:
        raise ValueError()
    pyproject = tomli.loads(pyproject_toml.read_text())
    conf_base = pyproject["tool"]["sphinx-build"][conf_py.parent.stem]
    caller.frame.f_locals.update(
        {k: v for k, v in conf_base.items() if not k.startswith("_")}
    )
