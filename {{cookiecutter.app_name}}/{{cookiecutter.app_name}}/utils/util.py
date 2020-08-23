from {{cookiecutter.app_name}}.models.user import AuthLog
from pyramid.security import remember


def remember_req(request, user, event='L'):
    ip_addr = request.client_addr
    record = AuthLog(user_id=user.id,
                     ip_addr=ip_addr,
                     event=event)
    request.dbsession.add(record)
    request.dbsession.flush()
    return remember(request, user.id)
