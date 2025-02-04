"""TTS gneration by Voicepeak."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Union

from . import Options, Provider


class VoicepeakOptions(Options):
    execute_path: Union[Path, str]


@dataclass
class VoicepeakProvider(Provider):
    format: ClassVar[str] = "wav"
    options: VoicepeakOptions

    def load(self):
        pass

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
