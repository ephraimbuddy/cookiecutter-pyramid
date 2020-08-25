from {{cookiecutter.app_name}}.views.user.auth import register


def test_register_view_runs_successful(testapp):
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


