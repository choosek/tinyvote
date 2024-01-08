========
tinyvote
========

Minimal pure-Python library that demonstrates a basic encrypted voting workflow via a secure multi-party computation (MPC) `protocol <https://eprint.iacr.org/2023/1740>`__.

|pypi|

.. |pypi| image:: https://badge.fury.io/py/tinyvote.svg
   :target: https://badge.fury.io/py/tinyvote
   :alt: PyPI version and link.

Purpose
-------

This library demonstrates how a functionality can be implemented using a `secure multi-party computation (MPC) protocol <https://eprint.iacr.org/2023/1740>`__ for evaluating arithmetic sum-of-products expressions (as implemented in `tinynmc <https://pypi.org/project/tinynmc>`__). The approach used in this library can serve as a template for any workflow that relies on multiple simultaneous instances of such a protocol.

Installation and Usage
----------------------

This library is available as a `package on PyPI <https://pypi.org/project/tinyvote>`__:

.. code-block:: bash

    python -m pip install tinyvote

The library can be imported in the usual way:

.. code-block:: python

    import tinyvote
    from tinyvote import *

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__:

.. code-block:: bash

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__:

.. code-block:: bash

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details):

.. code-block:: bash

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__:

.. code-block:: bash

    python src/tinyvote/tinyvote.py -v

Style conventions are enforced using `Pylint <https://pylint.readthedocs.io>`__:

.. code-block:: bash

    python -m pip install .[lint]
    python -m pylint src/tinyvote

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/choosek/tinyvote>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/tinyvote>`__ by a package maintainer. First, install the dependencies required for packaging and publishing:

.. code-block:: bash

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Create and push a tag for this version (replacing ``?.?.?`` with the version number):

.. code-block:: bash

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive:

.. code-block:: bash

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__:

.. code-block:: bash

    python -m twine upload dist/*