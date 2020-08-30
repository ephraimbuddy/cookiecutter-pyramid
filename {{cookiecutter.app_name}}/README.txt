{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

Getting Started
---------------

- Change directory into your newly created project.

    cd {{ cookiecutter.app_name }}

- Create a Python virtual environment.

    python3 -m venv env

- Activate your virtual env

  For linux based:

  $ source env/bin/activate

  For windows, activate with:
      env\Scripts\activate

- Upgrade packaging tools.

    pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    pip install -e ".[testing]"

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

       alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

       alembic -c development.ini upgrade head

- Load default data into the database using a script.

    initdb development.ini

- Run your project's tests.

    pytest

- Run your project.

    pserve development.ini
