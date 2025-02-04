"""TTS gneration by Amazon polly."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import boto3

from . import Options, Provider

if TYPE_CHECKING:
    from mypy_boto3_polly.client import PollyClient
else:
    PollyClient = object


class PollyOptions(Options):
    engine: str = "standard"
    voice_id: str = "Matthew"


@dataclass
class PollyProvider(Provider):
    format: ClassVar[str] = "mp3"
    options: PollyOptions
    client: PollyClient = field(init=False)

    def load(self):
        self.client = boto3.client("polly")

    def generate_audio(self, text: str, out: Path, extra: dict = {}):
        resp = self.client.synthesize_speech(
            Engine=self.options.engine,  # type: ignore[arg-type]
            OutputFormat=self.format,  # type: ignore[arg-type]
            Text=text,
            VoiceId=self.options.voice_id,  # type: ignore[arg-type]
        )
        out.write_bytes(resp["AudioStream"].read())
