import unittest
from datetime import datetime

from pyramid.testing import DummyRequest
from pyrasatest import MockModel, PartialMockDbSession
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, scoped_session

from pyratest.models import Account, Order, Product
from pyratest.models.meta import Base
from pyratest.views.default import OrderInfoView


class OrderInfoViewTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        cls.session = scoped_session(sessionmaker(bind=engine))
        Base.metadata.create_all(engine)
        request = DummyRequest()
        request.dbsession = cls.session
        cls.view = OrderInfoView(request)
        acc1 = Account(name='dep3', number='123')
        acc2 = Account(name='no2', number='124')
        cls.accounts = [acc1, acc2]
        for acc in cls.accounts:
            setattr(acc, 'acc_num', 5)
        cls.session.add_all(cls.accounts)
        cls.session.commit()
        ord1 = Order(reference='foo', account_id=acc1.id, date=datetime.now())
        ord2 = Order(reference='bar', account_id=acc2.id, date=datetime.now())
        cls.orders = [ord1, ord2]
        prd1 = Product(number='323', price=10.40)
        prd2 = Product(number='542', price=7.80)
        cls.products = [prd1, prd2]
        cls.session.add_all(cls.orders + cls.products)
        cls.session.commit()

    def test_get_orders_for_account_order_ids_query_mocked(self):
        self.view.request.params.update({
            'product_char': self.products[0].number[0]
        })
        mocked_order_results = [MockModel(id=i, reference=s)
                                for i, s in enumerate(['ab', 'bc', 'cd'])]
        self.view.request.dbsession = PartialMockDbSession(
            query_return_values={Order.id: mocked_order_results},
            dbsession=self.session
        )
        expected_output = {
            'orders': [f'{a.id} - {a.reference}' for a in mocked_order_results],
            'product_results':
                [f'{a.id} - {a.number}' for a in self.products if
                 self.view.request.params['product_char'] in a.number]
        }
        self.assertEqual(expected_output,
                         self.view.get_orders_for_account())

    def test_get_orders_for_account_product_results_query_mocked(self):
        self.view.request.params.update({
            'account_name': self.accounts[0].name,
            'product_char': self.products[0].number[0]
        })
        mocked_product_results = [MockModel(id=i, number=s)
                                  for i, s in enumerate(['12', '34', '56'])]
        self.view.request.dbsession = PartialMockDbSession(
            query_return_values={Product.id: mocked_product_results},
            dbsession=self.session
        )
        expected_output = {
            'orders': [f'{a.id} - {a.reference}' for a in self.orders
                       if a.account_id == self.accounts[0].id],
            'product_results':
                [f'{a.id} - {a.number}' for a in mocked_product_results]
        }
        self.assertEqual(expected_output,
                         self.view.get_orders_for_account())

    def test_get_account_and_product_number(self):
        self.view.request.params.update({
            'account_id': self.accounts[0].id,
            'product_id': self.products[0].id
        })
        acc_name = self.accounts[0].name
        acc_num = self.accounts[0].number
        pn = self.products[0].number
        self.assertEqual(
            {'account_name': acc_name,
             'account_number': acc_num,
             'product_number': pn},
            self.view.get_account_and_product_number()
        )

    def test_get_account_and_product_number_with_mocked_account_query(self):
        self.view.request.params = {'account_id': self.accounts[0].id}
        acc_data = {'name': 'foo', 'acc_num': 45}
        mock_account = MockModel(**acc_data)
        self.view.request.dbsession = PartialMockDbSession(
            query_return_values={Account.number.label('acc_num'): mock_account},
            dbsession=self.session
        )
        self.assertEqual(
            {'account_name': acc_data['name'],
             'account_number': acc_data['acc_num'],
             'product_number': None},
            self.view.get_account_and_product_number()
        )

    def test_get_account_and_product_number_with_mocked_product_query(self):
        self.view.request.params = {'account_id': self.accounts[0].id}
        mock_product = MockModel(id=32)
        self.view.request.dbsession = PartialMockDbSession(
            query_return_values={Product.number: mock_product},
            dbsession=self.session
        )
        self.assertEqual(
            {'account_name': self.accounts[0].name,
             'account_number': self.accounts[0].number,
             'product_number': mock_product[0]},
            self.view.get_account_and_product_number()
        )
