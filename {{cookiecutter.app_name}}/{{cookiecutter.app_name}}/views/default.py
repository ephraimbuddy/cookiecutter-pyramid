from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from {{cookiecutter.app_name}}.models.user import User


@view_config(route_name='home', renderer='{{ cookiecutter.app_name }}:templates/mytemplate.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def index(request):
    try:
        user = request.dbsession.query(User).one()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'user': user, 'project': '{{ cookiecutter.project_name }}'}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
