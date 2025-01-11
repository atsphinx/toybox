=========================
atsphinx.toybox.pyproject
=========================

.. note:: Added by v2025.1.11

Overview
========

This is configuration loader from ``pyproject.toml``.

Usage
=====

Use case
--------

.. code-block:: text
   :caption: Example workspace

   /ProjectRoot
     - pyproject.toml
     - docs/
       - conf.py

1. Write your coufiguration into ``pyproject.toml`` from ``conf.py``.

   .. code-block:: toml
      :caption: pyproject.toml

      # Root section is "tool.sphinx-build.YOUR_DOCUMENT_DIR"
      [tool.sphinx-build.docs]
      copyright = "2024, Kazuya Takei"

      # -- General configuration
      extensions = [
          # Set extensions...
      ]

   .. important::

      Currently, this supports TOML's raw values.

2. Write your coufiguration into ``pyproject.toml`` from ``conf.py``.

   .. code-block:: python
      :caption: conf.py

      from atsphinx.toybox.pyproject import load

      load()

3. Build like always.

   .. code-block:: console

      make html
