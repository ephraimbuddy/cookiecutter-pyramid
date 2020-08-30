from {{ cookiecutter.app_name }}.views.default import home


def test_index_success(app_request):
    info = home(app_request)
    assert app_request.response.status_int == 200
    assert info['project'] == '{{ cookiecutter.project_name }}'


