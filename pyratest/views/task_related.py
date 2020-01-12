from urllib.parse import urlparse

from celery.exceptions import TimeoutError
from pyramid.response import Response
from pyramid.view import view_config

from pyratest.tasks.accounts import account_task
from pyratest.tasks.notifier import notifier_task


@view_config(route_name='account_task',
             renderer='../templates/task_id_form.mako')
def account_task_view(request):
    task_id = request.params.get('task_id')
    if not task_id:
        task = account_task.delay()
        return {'task_id': task.id, 'result': 'n/a'}

    task_result = account_task.AsyncResult(task_id)
    try:
        result = task_result.get(timeout=12)
        print(result)
        return {'task_id': task_id, 'result': result}
    except TimeoutError:
        print('got timeout')
        return {'task_id': task_id, 'result': 'n/a'}


@view_config(route_name='notifier', renderer='../templates/notifier_task.mako')
def notifier_view(request):
    client_id = request.params.get('clientid')
    if request.method == 'POST' and client_id:
        notifier_task.delay(clientid=client_id)
        return Response(
            body='waiting for result',
            status='202 Accepted',
            content_type='application/json; charset=UTF-8'
        )
    return {
        'notifier_url': 'http://{}:{}'.format(
            urlparse(request.url).hostname, 3000),
    }
