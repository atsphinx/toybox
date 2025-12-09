"""Tokenize override by Lindera."""

from lindera_py import (
    Segmenter,  # type: ignore[unresolved-import]
    Tokenizer,  # type: ignore[unresolved-import]
    load_dictionary,  # type: ignore[unresolved-import]
)
from sphinx.search.ja import BaseSplitter


class LinderaSplitter(BaseSplitter):
    """Simple splitter class using Lindera as tokeniser."""

    def __init__(self, options: dict[str, str]) -> None:  # noqa: D107
        self.dictionary = load_dictionary("ipadic")
        self.segmenter = Segmenter("normal", self.dictionary)
        self.tokenizer = Tokenizer(self.segmenter)

    def split(self, input: str) -> list[str]:  # noqa: D102
        return [token.text for token in self.tokenizer.tokenize(input)]
