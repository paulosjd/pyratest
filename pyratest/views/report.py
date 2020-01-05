from pyramid.view import view_config

from .. import models
from pyratest.tasks.orders_report import mytask

template_path = '../templates/mytemplate.mako'


@view_config(route_name='report', renderer=template_path)
def my_view(request):
    foobar = request.dbsession.query(models.Account).filter(
        models.Account.name == 'Foobar Ltd').first()
    mytask.delay()
    return {'one': foobar}
