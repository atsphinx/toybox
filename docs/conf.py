from atsphinx.toybox.pyproject import load
from atsphinx.toybox.stlite import DEFAULT_STLITE_VERSION

load()

rst_prolog = f"""
.. |default_stlite_version| replace:: ``"{DEFAULT_STLITE_VERSION}"``
"""
