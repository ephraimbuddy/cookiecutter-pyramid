About This Fork🍴
=================
This is a fork of https://github.com/Pylons/pyramid-cookiecutter-starter with decisions made on the
type of persistent backend and url mapping scheme to use, with session management, authentication
and authorization features.

cookiecutter-pyramid
============================

.. image:: https://travis-ci.org/ephraimbuddy/cookiecutter-pyramid.png?branch=dev
    :target: https://travis-ci.org/ephraimbuddy/cookiecutter-pyramid
    :alt: Dev Travis CI Status

A Cookiecutter (project template) for creating a Pyramid starter project.

Customizable options upon install include choice of:

*   template language (Jinja2, Chameleon, or Mako)

Decisions made for you:

* Session management with `pyramid_nacl_session <https://docs.pylonsproject.org/projects/pyramid-nacl-session/en/latest/index.html>`_
* SQLAlchemy as the ORM
* WTForms as form library
* Bootstrap 4
* Automatic csrf protection
* Inbuilt Authentication and Authorization mechanism

Requirements
------------

*   Python 3.5+
*   `cookiecutter <https://cookiecutter.readthedocs.io/en/latest/installation.html>`_

Versions
--------

This cookiecutter has several branches to support new features in Pyramid or avoid incompatibilities.

*   ``master`` aligns with the latest stable release of Pyramid, and is the default branch on GitHub.
*   ``dev`` aligns with the ``master`` branch of Pyramid, and is where development takes place.
*   ``x.y-branch`` aligns with the ``x.y-branch`` branch of Pyramid.


Usage
-----

#.  Generate a Pyramid project, following the prompts from the command.

    .. code-block:: bash

        $ cookiecutter gh:ephraimbuddy/cookiecutter-pyramid

    Optionally append a specific branch checkout to the command:

    .. code-block:: bash

        $ cookiecutter gh:ephraimbuddy/cookiecutter-pyramid --checkout dev

#.  Create a virtual environment, upgrade packaging tools, and install your new project and its dependencies.
    These steps are output by the cookiecutter and are written to the file in ``<my_project>/README.txt``, and are slightly different for Windows.

    .. code-block:: bash

        # Change directory into your newly created project.
        $ cd <my_project>
        # Create a Python virtual environment.
        $ python3 -m venv env
        # Activate the virtual environment.
        $ source env/bin/activate
        # For windows, activate with:
          env\Scripts\activate
        # Upgrade packaging tools.
        $ pip install --upgrade pip setuptools
        # Install the project in editable mode with its testing requirements.
        $ pip install -e ".[testing]"
        # Generate your first revision
        $ alembic -c development.ini revision --autogenerate -m "init"
        # Upgrade the revision
        $ alembic -c development.ini upgrade head
        # Load default data into the database using a script.
        $ initdb development.ini


#.  Run your project's tests.

    .. code-block:: bash

        $ pytest

#.  Run your project.

    .. code-block:: bash

        $ pserve development.ini
