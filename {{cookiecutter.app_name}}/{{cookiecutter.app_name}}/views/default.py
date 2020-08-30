from pyramid.view import view_config


@view_config(route_name='home', renderer='{{ cookiecutter.app_name }}:templates/home.{{ "pt" if "chameleon" == cookiecutter.template_language else cookiecutter.template_language }}')
def home(request):

    return {'project': '{{ cookiecutter.project_name }}'}
