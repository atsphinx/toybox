import os

from atsphinx.toybox.pyproject import load
from atsphinx.toybox.stlite import DEFAULT_STLITE_VERSION

load()

rst_prolog = f"""
.. |default_stlite_version| replace:: ``"{DEFAULT_STLITE_VERSION}"``
"""

tts_provider = "voicepeak"
tts_options = {
    "execute_path": os.environ.get(
        "VOICEPEAK_PATH", "/home/attakei/.local/opt/voicepeak/voicepeak"
    )
}
