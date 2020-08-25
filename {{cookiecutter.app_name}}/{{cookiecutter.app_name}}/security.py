from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone, Authenticated
from {{cookiecutter.app_name}}.models.user import User, RootFactory



class AuthenticationPolicy(AuthTktAuthenticationPolicy):
    """ AuthenticationPolicy to avoid blindly trusting the value in cookie"""
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

    def effective_principals(self, request):
        principals = [Everyone]
        userid = self.authenticated_userid(request)
        if userid:
            principals += [Authenticated, str(userid)]
        return principals

def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id:
        user = request.dbsession.query(User).get(user_id)
        return user

def group_finder(userid, request):
    user = request.dbsession.query(User).get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]


def includeme(config):
    config.include('pyramid_nacl_session')
    settings = config.get_settings()
    authn_policy = AuthenticationPolicy(
        settings['auth.secret'],
        hashalg='sha512', callback=group_finder
    )
    authz_policy = ACLAuthorizationPolicy()
    config.add_request_method(get_user, 'user', reify=True)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_csrf_options(require_csrf=True)
    config.set_root_factory(RootFactory)
    
