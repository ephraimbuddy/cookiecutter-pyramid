from {{ cookiecutter.app_name }}.models.user import User
from {{ cookiecutter.app_name }}.views.default import index
from {{ cookiecutter.app_name }}.views.notfound import notfound_view


def test_index_failure(app_request):
    info = index(app_request)
    assert info.status_int == 500

def test_index_success(app_request, dbsession):
    user = User(username='username', password='password', email='foo@bar.com')
    dbsession.add(user)
    dbsession.flush()

    info = index(app_request)
    assert app_request.response.status_int == 200
    assert info['user'] == user
    assert info['project'] == '{{ cookiecutter.project_name }}'

def test_notfound_view(app_request):
    info = notfound_view(app_request)
    assert app_request.response.status_int == 404
    assert info == {}
