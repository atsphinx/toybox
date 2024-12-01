from pathlib import Path

from atsphinx.mini18n import get_template_dir as get_mini18n_template_dir
from atsphinx.toybox import __version__ as version

root = Path(__file__).parent

# -- Project information
project = "atsphinx-toybox"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    # Bundled extensions
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # Third-party extensions
    "atsphinx.mini18n",
    # My extensions
    "atsphinx.toybox.sass",
    "atsphinx.toybox.stlite",
]
templates_path = ["_templates", get_mini18n_template_dir()]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "node_modules"]

# -- Options for i18n
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_theme = "furo"
html_static_path = ["_static"]
html_title = f"{project} v{release}"
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/atsphinx/toybox/",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
}
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "mini18n/snippets/select-lang.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# -- Options for extensions
# sphinx.ext.intersphinx
intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
# sphinx.ext.todo
todo_include_todos = True
# atsphinx.mini18n
mini18n_default_language = "en"
mini18n_support_languages = ["en", "ja"]
mini18n_basepath = "/toybox/"
# atsphinx.toybox.sass
sass_load_paths = [root / "node_modules"]
sass_extra_options = ["--update", "-q"]


def setup(app):
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
