"""Sass autobuild.

Spec
====

* Use dart-sass binary
* Auto find ``_sass`` directory.
* Exclude ``_`` prefixed files.
* Copy into _static
* Timestamp based incremental build.
"""

from pathlib import Path

from sphinx.application import Sphinx

from . import dart_sass

SASS_VERSION = "1.81.0"

package_root = Path(__file__).parent

bin_dist = package_root / "_bin"


def setup(app: Sphinx):  # noqa: D103
    dart_sass.setup_dart_sass(SASS_VERSION, bin_dist)
    return {}
