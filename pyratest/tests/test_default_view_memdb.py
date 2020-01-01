from datetime import datetime
import unittest

from pyramid.testing import DummyRequest
from pyrasatest import MockModel, MockQuery, MockRequest
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

    def test_get_orders_for_account_with_product_char_falsey(self):
        self.view.request.params.update({'account_name': self.accounts[0].name})
        self.assertEqual(
            {'orders': [f'{a.id} - {a.reference}' for a in self.orders
                        if a.account_id == self.accounts[0].id]},
            self.view.get_orders_for_account()
        )
        # SITUTATIONS WHERE WANT TO PART-MOCK E.G. TWO QUERIES - FIRST ONE (ABOVE)
        # WANT TO RUN NORMALLY BUT THEN NEXT WANT TO USE MOCK QUERY FOR SELF.REQUEST.DBSESSION (OR VICE VERSA)

    def test_get_orders_for_account_with_product_char_truthy(self):
        self.view.request.params.update({
            'account_name': self.accounts[0].name,
            'product_char': self.products[0].number[0]
        })
        expected_output = {
            'orders': [f'{a.id} - {a.reference}' for a in self.orders
                       if a.account_id == self.accounts[0].id],
            'product_results':
                [f'{a.id} - {a.number}' for a in self.products if
                 self.view.request.params['product_char'] in a.number]
        }
        self.assertEqual(expected_output,
                         self.view.get_orders_for_account())

