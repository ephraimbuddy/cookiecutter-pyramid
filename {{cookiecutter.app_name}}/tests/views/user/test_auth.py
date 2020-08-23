from {{cookiecutter.app_name}}.views.user.auth import register


def test_register(app_request):
    view = register(app_request)
    