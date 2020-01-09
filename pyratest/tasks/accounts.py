import time

from pyratest.models import Account
from pyratest.tasks.celery_app import celery_app
from pyratest.tasks.celery_db_session import db_session


@celery_app.task
def account_task():
    """ Simulates some slow computation """
    time.sleep(5)
    acc = db_session.query(Account).first()
    return f'Account: {acc.number} - {acc.name}'
