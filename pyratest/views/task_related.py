import time

from celery.exceptions import TimeoutError
from pyramid.view import view_config

from pyratest.models import Account
from pyratest.tasks.orders_report import mytask1, mytask2, mytask3

template_path = '../templates/mytemplate.mako'


@view_config(route_name='report1', renderer=template_path)
def my_view1(request):
    foobar = request.dbsession.query(Account).filter(
        Account.name == 'Foobar Ltd').first()
    task = mytask1.delay()
    task_id = task.id
    print(task_id)
    return {'one': foobar}


@view_config(route_name='report2', renderer=template_path)
def my_view2(request):
    task_id = request.params.get('task_id',
                                 'b2ea3c69-ea14-4355-b6c6-949f5d4eb8ff')
    if task_id:
        task_result = mytask1.AsyncResult(task_id)
        try:
            result = task_result.get(timeout=40)
            print(result)
        except TimeoutError:
            print('got timeout')

    return {'one': 'a'}


@view_config(route_name='report3', renderer=template_path)
def my_view3(request):
    foobar = request.dbsession.query(Account).filter(
        Account.name == 'Foobar Ltd').first()
    mytask1.delay()
    return {'one': foobar}
