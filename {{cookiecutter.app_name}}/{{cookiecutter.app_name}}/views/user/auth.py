from pyramid.view import view_config
from pyramid.security import forget, remember
from pyramid.httpexceptions import HTTPFound, HTTPSeeOther

from {{cookiecutter.app_name}}.forms.user.auth import RegistrationForm, LoginForm
from {{cookiecutter.app_name}}.models.user import User


@view_config(route_name='registration', renderer='{{ cookiecutter.app_name }}:templates/user/registration.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def register(request):
    if request.user:
        request.session.flash("info; You are already logged in")
        return HTTPSeeOther(location='/')
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        username_exists = User.by_username(request.dbsession, form.username.data)
        if username_exists:
            msg = "The selected username is not available"
            form.username.errors.append(msg)
            return dict(form=form, title="Account Registration")
        email_exists = User.by_email(request.dbsession, form.email.data)
        if email_exists:
            msg = "You are already registered"
            form.email.errors.append(msg)
            return dict(form=form, title="Account Registration")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        request.dbsession.add(user)

        headers = remember(request, user.id)
        return HTTPFound(location=request.route_url('home'), headers=headers)
    return dict(form=form, title="Account Registration")


@view_config(route_name="login", renderer='{{ cookiecutter.app_name }}:templates/user/login.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def login(request):
    if request.user:
        request.session.flash("info; You're already signed in")
        return HTTPFound(location=request.route_url('home'))
    form = LoginForm(request.POST)
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user = User.by_username(request.dbsession, username)
        if user and user.verify_password(form.password.data):
            headers = remember(request, user.id)
            return HTTPFound(location=came_from, headers=headers)

        message = 'Failed login, Please try again'
        return dict(form=form, message=message,
                    came_from=came_from, title="User Login")
    return dict(form=form, message=message, came_from=came_from,
                 title="User Login")


@view_config(route_name="logout", renderer="string")
def logout(request):
    headers = forget(request)
    request.session.invalidate()
    return HTTPFound(location='/', headers=headers)
