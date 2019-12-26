
from pyramid.response import Response
from pyramid.view import view_config

from .. import models


@view_config(route_name='home', renderer='../templates/mytemplate.mako')
def my_view(request):
    query = request.dbsession.query(models.Order)
    one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': one, 'project': 'pyratest'}


@view_config(route_name='home', renderer='../templates/mytemplate.mako')
def my_view(request):
    query = request.dbsession.query(models.Order)
    one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': one, 'project': 'pyratest'}

