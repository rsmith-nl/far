Find and Replace
################

:date: 2020-10-27
:tags: python3
:author: Roland Smith

.. Last modified: 2022-01-29T22:25:32+0100

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Introduction
------------

This is a simple GUI to find a file in a directory tree by name and replace it by
another file. It is mainly meant for ms-windows which lacks the ``find``
program available on POSIX systems.


Requirements
------------

* Python 3.6+
* Tkinter

(Most Python distributions for ms-windows include tkinter.)


Installation
------------

To install it for the local user, run::

    python setup.py install

This will install it in the user path for Python scripts.
For POSIX operating systems this is ususally ``~/.local/bin``.
For ms-windows this is the ``Scripts`` directory of your Python installation
or another local directory.
Make sure that this directory is in your ``$PATH`` environment variable.


License
-------

MIT. See LICENSE.txt
