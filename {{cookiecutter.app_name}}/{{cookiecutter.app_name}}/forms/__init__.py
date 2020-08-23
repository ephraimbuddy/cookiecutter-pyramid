from wtforms.csrf.session import SessionCSRF
from pyramid.threadlocal import get_current_registry
from datetime import timedelta
from wtforms import Form

strip_filter = lambda x: x.strip() if x else None


class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = get_current_registry().settings['csrf.secret']
        csrf_time_limit = timedelta(minutes=15)
