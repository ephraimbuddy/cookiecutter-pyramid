import os
import pytest
import sys
import subprocess
import textwrap

WIN = sys.platform == 'win32'
WORKING = os.path.abspath(os.path.join(os.path.curdir))

project_files = [
    '.coveragerc',
    '.gitignore',
    '/myapp/__init__.py',
    '/myapp/alembic/env.py',
    '/myapp/alembic/script.py.mako',
    '/myapp/alembic/versions/README.txt',
    '/myapp/forms/__init__.py',
    '/myapp/forms/user/__init__.py',
    '/myapp/forms/user/auth.py',
    '/myapp/models/__init__.py',
    '/myapp/models/meta.py',
    '/myapp/models/user.py',
    '/myapp/pshell.py',
    '/myapp/routes.py',
    '/myapp/scripts/__init__.py',
    '/myapp/scripts/initialize_db.py',
    '/myapp/security.py',
    '/myapp/static/pyramid-16x16.png',
    '/myapp/static/pyramid.png',
    '/myapp/static/theme.css',
    '/myapp/templates/404.template_extension',
    '/myapp/templates/layout.template_extension',
    '/myapp/templates/mytemplate.template_extension',
    '/myapp/templates/user/login.template_extension',
    '/myapp/templates/user/registration.template_extension',
    '/myapp/utils/__init__.py',
    '/myapp/utils/util.py',
    '/myapp/views/__init__.py',
    '/myapp/views/default.py',
    '/myapp/views/notfound.py',
    '/myapp/views/user/__init__.py',
    '/myapp/views/user/auth.py',
    '/tests/__init__.py',
    '/tests/conftest.py',
    '/tests/models/__init__.py',
    '/tests/models/test_user.py',
    '/tests/views/__init__.py',
    '/tests/views/test_default.py',
    '/tests/views/test_functional.py',
    '/tests/views/test_notfound.py',
    '/tests/views/user/__init__.py',
    '/tests/views/user/test_auth.py',
    'CHANGES.txt',
    'MANIFEST.in',
    'README.txt',
    'development.ini',
    'production.ini',
    'pytest.ini',
    'setup.py',
    'testing.ini',
]


def build_files_list(root_dir):
    """Build a list containing relative paths to the generated files."""
    file_list = []
    for dirpath, subdirs, files in os.walk(root_dir):
        for file_path in files:
            file_list.append(os.path.join(dirpath[len(root_dir):], file_path))

    return file_list


@pytest.mark.parametrize('template', ['jinja2', 'mako', 'chameleon'])
def test_project(cookies, venv, capfd, template):
    result = cookies.bake(extra_context={
        'project_name': 'Test Project',
        'template_language': template,
        'app_name': 'myapp',
    })

    assert result.exit_code == 0

    out, err = capfd.readouterr()

    if WIN:
        assert 'Scripts\\pserve' in out
        for idx, project_file in enumerate(project_files):
            project_files[idx] = project_file.replace('/', '\\')
        project_files.sort()
    else:
        assert 'bin/pserve' in out

    files = build_files_list(str(result.project))
    files.sort()

    # Rename files based on template being used
    if template == 'chameleon':
        template = 'pt'

    for idx, sqlalchemy_file in enumerate(project_files):
        if 'templates' in sqlalchemy_file:
            project_files[idx] = project_files[idx].split('.')[
                                     0] + '.' + template

    assert project_files == files

    cwd = result.project.strpath

    # this is a hook for executing scaffold tests against a specific
    # version of pyramid (or a local checkout on disk)
    if 'OVERRIDE_PYRAMID' in os.environ:  # pragma: no cover
        venv.install(os.environ['OVERRIDE_PYRAMID'], editable=True)

    venv.install(cwd + '[testing]', editable=True)
    create_migration_script = textwrap.dedent(
        '''
        import alembic.config
        import alembic.command

        config = alembic.config.Config('testing.ini')
        alembic.command.revision(
            config,
            autogenerate=True,
            message='init',
        )
        '''
    )
    subprocess.check_call([venv.python, '-c', create_migration_script], cwd=cwd)
    subprocess.check_call([venv.python, '-m', 'pytest', '-q'], cwd=cwd)


def test_it_invalid_module_name(cookies, venv, capfd):
    result = cookies.bake(extra_context={
        'app_name': '0invalid',
    })
    assert result.exit_code == -1
