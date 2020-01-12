import unittest
from collections import namedtuple
from unittest.mock import patch
from urllib.parse import urlparse

from celery.exceptions import TimeoutError
from pyrasatest import MockRequest

from pyratest.tasks.accounts import account_task
from pyratest.tasks.notifier import notifier_task
from pyratest.views.task_related import account_task_view, notifier_view


class AccountsTasksTestCase(unittest.TestCase):
    def setUp(self):
        self.task_id = 'test_id'
        self.mock_request = MockRequest(params={'task_id': self.task_id})

    @patch.object(account_task, 'delay')
    def test_account_task_view_no_task_id(self, task_patch):
        mock_task = namedtuple('task', 'id')('test_id')
        task_patch.return_value = mock_task
        self.assertEqual(
            {'task_id': mock_task.id, 'result': 'n/a'},
            account_task_view(MockRequest())
        )

    @patch.object(account_task, 'AsyncResult')
    def test_account_task_view_task_id_in_params(self, async_result_patch):
        def mock_result_get(**kwargs):
            return 'test result'
        mock_async_result = namedtuple('mock_async_get', 'get')(mock_result_get)
        async_result_patch.return_value = mock_async_result
        self.assertEqual(
            {'task_id': self.task_id, 'result': mock_result_get()},
            account_task_view(self.mock_request)
        )

    @patch.object(account_task, 'AsyncResult')
    def test_account_task_view_task_id_in_params_timeout_error(self, cel_patch):
        def mock_result_get(**kwargs):
            raise TimeoutError
        mock_async_result = namedtuple('mock_async_get', 'get')(mock_result_get)
        cel_patch.return_value = mock_async_result
        self.assertEqual(
            {'task_id': self.task_id, 'result': 'n/a'},
            account_task_view(self.mock_request)
        )

    @patch.object(notifier_task, 'delay')
    def test_notifier_view_post_method(self, task_patch):
        client_id = 'test_id'
        resp = notifier_view(MockRequest(params={'clientid': client_id},
                                         method='POST'))
        self.assertEqual(202, resp.status_code)
        task_patch.assert_called()

    def test_notifier_view_default(self):
        self.assertEqual(
            {'notifier_url': 'http://{}:{}'.format(
                urlparse(self.mock_request.url).hostname, 3000)},
            notifier_view(self.mock_request)
        )
