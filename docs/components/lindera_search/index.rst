==============================
atsphinx.toybox.lindera_search
==============================

.. note:: Added by v2024.12.10

Overview
========

This is to use Lindera search components of Sphinx.

Usage
=====

Install requires
----------------

This extension requires optional installation.
Please add 'lindera-search' option when you install it.

.. code-block:: console

   pip install 'atsphinx-toybox[lindera-search]'

Set configuration
-----------------

Add this into your ``conf.py`` of Sphinx.

.. code-block:: python
   :caption: conf.py

   html_search_options = {
       "type": "atsphinx.toybox.lindera_search.LinderaSplitter",
   }

Demo
====

.. todo: Write it.

Refs
====

* `lindera-py <https://pypi.org/project/lindera-py/>`_
