import unittest
from unittest.mock import patch

from pyrasatest import MockModel, MockQuery, MockRequest

from pyratest.tasks.accounts import account_task


class AccountsTasksTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_account = MockModel(number=123, name='foo')

    @patch('pyratest.tasks.accounts.db_session.query')
    def test_account_task(self, db_session_patch):
        db_session_patch.return_value = MockQuery(first_=self.mock_account)
        self.assertEqual(
            f'Account: {self.mock_account.number} - {self.mock_account.name}',
            account_task()
        )
