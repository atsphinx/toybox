====================
atsphinx.toybox.sass
====================

.. note:: Added by v2024.12.2

Overview
========

This compiles SASS/SCSS resources into css when run sphinx-build.
This it to embed Stlite content into your documents.

Usage
=====

Enable extension
----------------

Add this into your ``conf.py`` of Sphinx.

.. code-block:: python
   :caption: conf.py

   extensions = [
       "atsphinx.toybox.sass",
   ]

Configuration
-------------

There are not configuration options.

.. note:: I will add some optioons.

Demo
====

This content is used generated CSS from SASS.

.. code:: rst

   .. container:: sass-demo-bulma-content

      This paragraph is colored by "purplel".

.. literalinclude:: ../../_sass/demo.scss
   :caption: docs/_sass/demo.scss

Result:

.. container:: sass-demo-bulma-content

   This paragraph is colored by "purplel".

Refs
====

* `dart-sacc CLI <https://sass-lang.com/documentation/cli/dart-sass/>`_
* `Repository <https://github.com/sass/dart-sass/>`_
