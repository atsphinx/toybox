"""TTS gneration by Voicepeak."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Union

from . import Engine, Options


class VoicepeakOptions(Options):
    execute_path: Union[Path, str]


@dataclass
class VoicepeakEngine(Engine):
    format: ClassVar[str] = "wav"
    options: VoicepeakOptions

    def generate_audio(self, text: str, out: Path, extra: dict = {}):
        text_line = text.replace("\n", " ")
        command = [
            str(self.options["execute_path"]),
            "-s",
            f"'{text_line}'",
            "-o",
            str(out),
        ]
        return subprocess.run(command)
