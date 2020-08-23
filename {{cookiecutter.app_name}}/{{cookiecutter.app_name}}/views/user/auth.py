from pyramid.view import view_config
from pyramid.security import forget
from pyramid.httpexceptions import HTTPFound

from {{cookiecutter.app_name}}.forms.user.auth import RegistrationForm, LoginForm
from {{cookiecutter.app_name}}.models.user import User
from {{cookiecutter.app_name}}.utils.util import remember_req


@view_config(route_name='registration', renderer='{{ cookiecutter.app_name }}:templates/user/registration.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def register(request):
    msg = ''
    if request.user:
        request.session.flash("info; You are already logged in")
        return HTTPFound(location='/')
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        username_exists = User.by_username(request.dbsession, form.username.data)
        if username_exists:
            msg = "The selected username is not available"
            return dict(form=form, msg=msg, title="Account Registration")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )
        request.dbsession.add(user)

        headers = remember_req(request, user, event='R')
        return HTTPFound(location=request.route_url('home'), headers=headers)
    return dict(form=form, msg=msg, title="Account Registration")


@view_config(route_name="login", renderer='{{ cookiecutter.app_name }}:templates/user/login.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def sign_in(request):
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
    error_cls = ''
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user = User.by_username(request.dbsession, username)
        if user and user.verify_password(form.password.data):
            headers = remember_req(request, user)
            return HTTPFound(location=came_from, headers=headers)

        message = 'Failed login, Please try again'
        error_cls = 'has-error'
        return dict(form=form, message=message, error_cls=error_cls,
                    came_from=came_from, title="User Login")
    return dict(form=form, message=message, came_from=came_from,
                error_cls=error_cls, title="User Login")


@view_config(route_name="signout", renderer="string")
def signout(request):
    headers = forget(request)
    request.session.invalidate()
    return HTTPFound(location='/', headers=headers)
