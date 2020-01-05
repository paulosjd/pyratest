import time

from pyratest.models import Account
from pyratest.tasks.celery_app import celery_app
from pyratest.tasks.celery_db_session import db_session


@celery_app.task
def mytask():
    """ Simulates some slow computation """
    time.sleep(2)
    ob = db_session.query(Account).all()
    print(list(ob))
    return 42
