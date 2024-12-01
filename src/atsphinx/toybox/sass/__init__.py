"""Sass autobuild.

Spec
====

* Use dart-sass binary
* Auto find ``_sass`` directory.
* Exclude ``_`` prefixed files.
* Copy into _static
* Timestamp based incremental build.
"""

import subprocess
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.config import Config

from . import dart_sass

SASS_VERSION = "1.81.0"

package_root = Path(__file__).parent

bin_dist = package_root / "_bin"
sass_bin: Path


def configure_sass_bin(app: Sphinx, config: Config):
    """Set up sass executable. It download binary if it needs."""
    global sass_bin
    sass_bin = dart_sass.setup_dart_sass(SASS_VERSION, bin_dist)


def compile_assets(app: Sphinx):
    """Compile assets (sass or scss to css)."""
    global sass_bin
    source_dir = app.srcdir / "_sass"
    output_dir = app.srcdir / "_static" / "css"
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [str(sass_bin), f"{source_dir}:{output_dir}"]
    subprocess.run(cmd)


def setup(app: Sphinx):  # noqa: D103
    app.connect("config-inited", configure_sass_bin)
    app.connect("builder-inited", compile_assets)
    return {}
