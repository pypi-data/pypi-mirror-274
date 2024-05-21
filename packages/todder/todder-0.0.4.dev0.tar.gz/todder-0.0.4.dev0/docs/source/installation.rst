=========================
Installation instructions
=========================

Installation
------------

The package works with Python 3.8+ and can be installed from both PyPI and conda-forge.

To install the package using the ``pip`` package manager, run the following command:

.. code:: bash

   $ python3 -m pip install todder


Run tests
---------

.. code:: bash

   $ pytest -vv -s -x --pdb


Build documentation
-------------------

.. code:: bash

   $ make -C docs/ html
