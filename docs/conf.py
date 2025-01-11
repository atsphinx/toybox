from atsphinx.mini18n import get_template_dir as get_mini18n_template_dir
from atsphinx.toybox.pyproject import load

# -- General configuration
templates_path = ["_templates", get_mini18n_template_dir()]

load()
