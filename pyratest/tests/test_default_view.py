import unittest

from pyrasatest import MockModel, MockQuery, MockRequest
from sqlalchemy import exc

from ..models import Account, Order, Product
from ..views.default import OrderInfoView


class OrderInfoViewTestCase(unittest.TestCase):
    def setUp(self):
        self.view = OrderInfoView(MockRequest())

    def test_get_order_info_order_not_found(self):
        self.view.request.dbsession.query_return_values = {
            Order: exc.SQLAlchemyError
        }
        self.assertEqual(
            {'status': 'order not found'},
            self.view.get_order_info()
        )

    def test_get_order_info_product_not_found(self):
        mock_order = MockModel(id=12)
        self.view.request.dbsession.query_return_values = {
            Order: mock_order,
            Product.id: exc.SQLAlchemyError
        }
        self.assertEqual(
            {'status': f'product not found for order id {mock_order.id}'},
            self.view.get_order_info()
        )

    def test_get_order_info_account_not_found(self):
        mock_order = MockModel(id=12)
        self.view.request.dbsession.query_return_values = {
            Order: mock_order,
            Product.id: MockModel(id=25),
            Account.name: exc.SQLAlchemyError
        }
        self.assertEqual(
            {'status': f'account not found for order id {mock_order.id}'},
            self.view.get_order_info()
        )

    def test_get_order_info(self):
        mock_order = MockModel(id=12, number=5)
        mock_product = MockModel(id=25)
        mock_account = MockModel(name='test_acc')
        query_return_values = {
            Order: mock_order,
            Product.id: mock_product,
            Account.name: mock_account
        }
        self.view.request.dbsession.query_return_values = query_return_values
        expected_output = {
            'status': 'ok',
            'order_number': mock_order.number,
            'product_id': mock_product[0],
            'account_name': mock_account[0],
        }
        self.assertEqual(expected_output, self.view.get_order_info())

    def test_get_account_info(self):
        mock_acc = MockModel(name='Abc', number='123')
        self.view.request.dbsession.return_value = MockQuery(first_=mock_acc)
        self.assertEqual(
            {'account_name': mock_acc.name, 'account_number': mock_acc.number},
            self.view.get_account_info()
        )

    def test_get_account_info_account_not_found(self):
        self.view.request.dbsession.return_value = MockQuery(
            first_=None,
            raise_exc=exc.SQLAlchemyError
        )
        self.assertEqual({}, self.view.get_account_info())

    def test_get_orders_for_account_with_product_char_falsey(self):
        mock_orders = [MockModel(**{'id': ind, 'reference': ref})
                       for ind, ref in enumerate(['ab', 'cd'])]
        self.view.request.dbsession.return_value = MockQuery(
            all_=mock_orders,
        )
        self.assertEqual({'orders': [f'{a[0]} - {a[1]}' for a in mock_orders]},
                         self.view.get_orders_for_account())

    def test_get_orders_for_account_with_product_char_truthy(self):
        mock_orders = [MockModel(**{'id': ind, 'reference': ref})
                       for ind, ref in enumerate(['ab', 'cd'])]
        mock_products = [MockModel(**{'id': ind, 'number': num})
                         for ind, num in enumerate(['123', '345'])]
        self.view.request.dbsession.side_effect = [
            MockQuery(all_=mock_orders),
            MockQuery(all_=mock_products)
        ]
        self.view.request.params.update({'product_char': '2'})
        self.assertEqual(
            {'orders': [f'{a[0]} - {a[1]}' for a in mock_orders],
             'products': [f'{a[0]} - {a[1]}' for a in mock_products]},
            self.view.get_orders_for_account()
        )


