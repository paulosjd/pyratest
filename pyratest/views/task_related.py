from urllib.parse import urlparse

from celery.exceptions import TimeoutError
from pyramid.response import Response
from pyramid.view import view_config

from pyratest.models import Account
from pyratest.tasks.notifier_task import notifier_task
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


@view_config(route_name='report2', renderer='../templates/task_id_form.mako')
def my_view2(request):
    task_id = request.params.get('task_id')
    if not task_id:
        task = mytask1.delay()
        return {'task_id': task.id, 'result': 'n/a'}

    task_result = mytask1.AsyncResult(task_id)
    try:
        result = task_result.get(timeout=12)
        print(result)
        return {'task_id': task_id, 'result': result}
    except TimeoutError:
        print('got timeout')
        return {'task_id': task_id, 'result': 'n/a'}


@view_config(route_name='report3', renderer='../templates/notifier_task.mako')
def my_view3(request):
    client_id = request.params.get('clientid')
    if request.method == 'POST' and client_id:
        notifier_task.delay(clientid=client_id)
        return Response(
            body='waiting for result',
            status='202 Accepted',
            content_type='application/json; charset=UTF-8'
        )
    return {
        'notifier_url': 'http://{}:{}'.format(urlparse(request.url).hostname,
                                              3000),
    }


@view_config(route_name='orders2', renderer='../templates/notifier_task.mako')
def mytask2_view(request):
    mytask2.delay()
    return {}


# @app.route('/runtask', methods=['POST'])
# def runtask():
#     """ Client receives id from notifier service upon connection. On a browser
#     click event, this is sent in the POST request body to this view function,
#     which then includes the client id as an argument for the Celery task. This
#     view function itself just returns a simple string in the 202 response """
#     clientid = request.form.get('clientid')
#     mytask.delay(clientid=clientid)
#     return 'running task...', 202
#

