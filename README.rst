========
tinyvote
========

Minimal pure-Python library that demonstrates a basic encrypted voting workflow by leveraging a secure multi-party computation (MPC) `protocol <https://eprint.iacr.org/2023/1740>`__.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/tinyvote.svg
   :target: https://badge.fury.io/py/tinyvote
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/tinyvote/badge/?version=latest
   :target: https://tinyvote.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/choosek/tinyvote/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/choosek/tinyvote/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/choosek/tinyvote/badge.svg?branch=main
   :target: https://coveralls.io/github/choosek/tinyvote?branch=main
   :alt: Coveralls test coverage summary.

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

Basic Example
^^^^^^^^^^^^^

.. |node| replace:: ``node``
.. _node: https://tinyvote.readthedocs.io/en/0.1.2/_source/tinyvote.html#tinyvote.tinyvote.node

Suppose that a secure decentralized voting workflow is supported by three parties. The |node|_ objects would be instantiated locally by each of these three parties:

.. code-block:: python

    >>> nodes = [node(), node(), node()]

The preprocessing workflow that the nodes must execute can be simulated. The number of voters that the workflow supports must be known, and it is assumed that all permitted choices are integers greater than or equal to ``0`` and strictly less than a fixed maximum value. The number of voters and the number of distinct choices can be supplied to the preprocessing simulation:

.. code-block:: python

    >>> preprocess(nodes, votes=4, choices=2)

Each voter must submit a request for the opportunity to submit a vote. Below, each of the four voters creates such a request:

.. code-block:: python

    >>> request_zero = request(identifier=0)
    >>> request_one = request(identifier=1)
    >>> request_two = request(identifier=2)
    >>> request_three = request(identifier=3)

Each voter can deliver a request to each node, and each node can then locally generate masks that can be returned to the requesting voter:

.. code-block:: python

    >>> masks_zero = [node.masks(request_zero) for node in nodes]
    >>> masks_one = [node.masks(request_one) for node in nodes]
    >>> masks_two = [node.masks(request_two) for node in nodes]
    >>> masks_three = [node.masks(request_three) for node in nodes]

.. |vote| replace:: ``vote``
.. _vote: https://tinyvote.readthedocs.io/en/0.1.2/_source/tinyvote.html#tinyvote.tinyvote.vote

Each voter can then generate locally a |vote|_ instance (*i.e.*, a masked vote choice):

.. code-block:: python

    >>> vote_zero = vote(masks_zero, 0)
    >>> vote_one = vote(masks_one, 1)
    >>> vote_two = vote(masks_two, 1)
    >>> vote_three = vote(masks_three, 1)

Every voter can broadcast its masked vote choice to all the nodes. Each node can locally assemble these as they arrive. Once a node has received all masked votes, it can determine its shares of the overall tally of the votes:

.. code-block:: python

    >>> shares = [
    ...     node.outcome([vote_zero, vote_one, vote_two, vote_three])
    ...     for node in nodes
    ... ]

.. |list| replace:: ``list``
.. _list: https://docs.python.org/3/library/functions.html#func-list

The overall outcome can be reconstructed from the shares by the voting workflow operator. The outcome is represented as a |list|_ in which each entry contains the tally for the choice corresponding to the entry's index:

.. code-block:: python

    >>> reveal(shares)
    [1, 3]

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

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number):

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
