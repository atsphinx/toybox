"""Tokenize override by Lindera."""
import io
import zipfile
from importlib.metadata import version
from pathlib import Path

import requests
from lindera import TokenizerBuilder  # type: ignore[unresolved-import]
from sphinx.search.ja import BaseSplitter

here = Path(__file__).parent


def try_fetch_dict() -> Path:  # noqa: D103
    lib_version = version("lindera-python")
    url = f"https://github.com/lindera/lindera/releases/download/v{lib_version}/lindera-ipadic-{lib_version}.zip"
    dict_path = here / f"lindera-ipadic-{lib_version}"
    if not dict_path.exists():
        dict_path.mkdir(exist_ok=True, parents=True)
        with (
            requests.get(url, allow_redirects=True) as res,
            io.BytesIO(res.content) as bytes_io,
            zipfile.ZipFile(bytes_io) as zip,
        ):
            zip.extractall(here)
        (here / "lindera-ipadic").rename(dict_path)
    return dict_path


class LinderaSplitter(BaseSplitter):
    """Simple splitter class using Lindera as tokeniser."""

    def __init__(self, options: dict[str, str]) -> None:  # noqa: D107
        dict_path = try_fetch_dict()
        builder = TokenizerBuilder()
        builder.set_mode("normal")
        builder.set_dictionary(str(dict_path))
        self.tokenizer = builder.build()

    def split(self, input: str) -> list[str]:  # noqa: D102
        return [token.surface for token in self.tokenizer.tokenize(input)]
