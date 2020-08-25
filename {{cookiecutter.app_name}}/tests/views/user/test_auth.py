from {{cookiecutter.app_name}}.views.user.auth import register
from {{cookiecutter.app_name}}.forms.user.auth import RegistrationForm
from {{cookiecutter.app_name}}.models.user import User


class TestRegistration:
    """ Test Registration"""

    def test_register_view(self, app_request):
        """ Test if we can visit the view"""
        info = register(app_request)
        assert isinstance(info['form'], RegistrationForm)
        assert info['title'] == 'Account Registration'

    def test_register_view_redirects_if_user_is_logged_in(self, app_request):
        # we return True below instead of user object for testing purposes
        app_request.user = True
        info = register(app_request)
        assert info.status_int == 303


    def test_can_register(
            self,
            testapp,
            dbsession
    ):
        response = testapp.get('/register')
        # get the registration form
        form = response.form
        # Fill it
        form['username'] = 'test-username'
        form['email'] = 'test@email.com'
        form['password'] = 'test-password'
        # Submit form
        response = form.submit().follow()
        assert response.status_int == 200
        user = User.by_id(dbsession, 1)
        assert user.email == 'test@email.com'




