import time

from celery.exceptions import TaskError

from pyratest.models import Account
from pyratest.tasks.celery_app import celery_app
from pyratest.tasks.celery_db_session import db_session


@celery_app.task
def mytask1():
    """ Simulates some slow computation,
    return - store rpc/backend string for temp_file_path or such (data from long slow compute)
                                 task_id,  error_message='',
    """
    time.sleep(6)
    ob = db_session.query(Account).all()
    print(list(ob))
    print('mytask1 called')
    return 'test_file_path_etc'


@celery_app.task
def mytask2():
    """ Simulates some slow computation,
    return - store rpc/backend string for temp_file_path or such (data from long slow compute)
                                 task_id,  error_message='',
    """
    time.sleep(5)
    acc = db_session.query(Account).first()
    return f'Account: {acc.number} - {acc.name}'


@celery_app.task
def mytask3():
    """ Simulates some slow computation,
    return - store rpc/backend string for temp_file_path or such (data from long slow compute)
                                 task_id,  error_message='',
    """
    time.sleep(5)
    ob = db_session.query(Account).all()
    print(list(ob))
    print('mytask3 called')

    return 'test_file_path_etc'


