from {{cookiecutter.app_name}}.views.user.auth import register, login
from {{cookiecutter.app_name}}.forms.user.auth import RegistrationForm, LoginForm
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
        users = dbsession.query(User).all()
        response = testapp.get('/')
        response = response.click('Create account')
        # get the registration form
        form = response.form
        # Fill it
        form['username'] = 'test-username'
        form['email'] = 'test@email.com'
        form['password'] = 'test-password'
        # Submit form
        res = form.submit()
        assert res.status_int == 302
        user = User.by_username(dbsession, 'test-username')
        assert user.email == 'test@email.com'
        assert dbsession.query(User).count() == len(users)+1

    def test_unique_username(self, testapp, dbsession):

        user = User(
            username='test-username',
            email='test@email.com',
            password='testpassword'
        )
        dbsession.add(user)
        # Go to home
        response = testapp.get('/')
        # Click create account
        response = response.click('Create account')
        # get the form
        form = response.form
        # Fill it
        form['username'] = 'test-username'  # same username
        form['email'] = 'test-email@email.com'
        form['password'] = 'test-password'
        # Submit form
        response = form.submit()
        assert 'Username already registered' in response

    def test_unique_email(self, testapp, dbsession):
        user = User(
            username='test-username',
            email='test@email.com',
            password='testpassword'
        )
        dbsession.add(user)
        # Go to home
        response = testapp.get('/')
        # Click create account
        response = response.click('Create account')
        # get the form
        form = response.form
        # Fill it
        form['username'] = 'test-username-2'
        form['email'] = 'test@email.com'  # Same email
        form['password'] = 'test-password'
        # Submit form
        response = form.submit()
        assert 'Email already registered' in response


class TestLogin:
    """ Test login"""

    def test_can_visit_login_view(self, app_request):
        info = login(app_request)
        assert isinstance(info['form'], LoginForm)
        assert info['title'] == 'User Login'
        assert info['came_from'] == 'http://example.com/'

    def test_login_view_redirects_if_user_is_logged_in(self, app_request):
        # we return True below instead of user object for testing purposes
        app_request.user = True
        info = login(app_request)
        assert info.status_int == 303

    def test_can_login(self, testapp, dbsession):
        user = User(
            username='test-user',
            email='test@email.com',
            password='test-password'
        )
        dbsession.add(user)
        # visit home page
        res = testapp.get('/')
        # click login button
        res = res.click('Log in')
        # get form
        form = res.form
        # fill it
        form['username'] = 'test-user'
        form['password'] = 'test-password'
        # submit
        res = form.submit()
        assert res.status_code == 303

    def test_wrong_username_gives_error(self, testapp, dbsession):
        user = User(
            username='test-user',
            email='test@email.com',
            password='test-password'
        )
        dbsession.add(user)
        # visit home page
        res = testapp.get('/')
        # click login button
        res = res.click('Log in')
        # get form
        form = res.form
        # fill it
        form['username'] = 'test-user-s'
        form['password'] = 'test-password'
        # submit
        res = form.submit()
        assert res.status_code == 200
        assert 'Failed login. Incorrect username or password' in res

    def test_wrong_password_gives_error(self, testapp, dbsession):
        user = User(
            username='test-user',
            email='test@email.com',
            password='test-password'
        )
        dbsession.add(user)
        # visit home page
        res = testapp.get('/')
        # click login button
        res = res.click('Log in')
        # get form
        form = res.form
        # fill it
        form['username'] = 'test-user'
        form['password'] = 'test-password-3'
        # submit
        res = form.submit()
        assert res.status_code == 200
        assert 'Failed login. Incorrect username or password' in res
        
