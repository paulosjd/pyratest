from pyramid.view import view_config
from sqlalchemy import exc

from .. import models

template_path = '../templates/mytemplate.mako'


@view_config(route_name='home', renderer=template_path)
def my_view(request):
    query = request.dbsession.query(models.Account)
    one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': one}


class OrderInfoView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='order_info', renderer=template_path)
    def get_order_info(self):
        try:
            order = self.request.dbsession.query(models.Order).filter(
                models.Order.id == self.request.params.get('order_id')).one()
        except exc.SQLAlchemyError:
            return {'status': 'order not found'}

        try:
            product_id = self.request.dbsession.query(models.Product.id).filter(
                models.Product.number == self.request.params.get(
                    'product_number')
            ).one()[0]
        except exc.SQLAlchemyError:
            return {'status': f'product not found for order id {order.id}'}

        try:
            acc_name = self.request.dbsession.query(models.Account.name).filter(
                models.Account.id == self.request.params.get('account_id')
            ).one()[0]
        except exc.SQLAlchemyError:
            return {'status': f'account not found for order id {order.id}'}

        return {
            'status': 'ok',
            'order_number': order.number,
            'product_id': product_id,
            'account_name': acc_name,
        }

    @view_config(route_name='account_info', renderer=template_path)
    def get_account_info(self):
        account = self.request.dbsession.query(models.Account).filter(
            models.Account.id == self.request.params.get('account_id')
        ).first()
        if not account:
            try:
                account = self.request.dbsession.query(models.Account).filter(
                    models.Account.name == 'guest'
                ).one()
            except exc.SQLAlchemyError:
                return {}
        return {'account_name': account.name, 'account_number': account.number}

    @view_config(route_name='account_orders', renderer=template_path)
    def get_orders_for_account(self):
        order_ids = self.request.dbsession.query(
            models.Order.id, models.Order.reference
        ).join(models.Account).filter(
            models.Account.name == self.request.params.get('account_name')
        ).all()
        order_data = {
            'orders': [f'{a.id} - {a.reference}' for a in order_ids]
        }
        if self.request.params.get('product_char'):
            product_results = self.request.dbsession.query(
                models.Product.id, models.Product.number
            ).filter(models.Product.number.contains(self.request.params.get(
                'product_char'))
            ).all()
            order_data.update({
                'product_results': [f'{a[0]} - {a[1]}' for a in product_results]
            })
        return order_data

    @view_config(route_name='acc_name_and_product', renderer=template_path)
    def get_account_and_product_number(self):
        acc_fields = self.request.dbsession.query(
            models.Account.number.label('acc_num'),
            models.Account.name,
        ).filter(
            models.Account.id == self.request.params.get('account_id')
        ).one()
        try:
            pn = self.request.dbsession.query(models.Product.number).filter(
                models.Product.id == self.request.params.get('product_id')
            ).one()[0]
        except exc.SQLAlchemyError:
            pn = None

        return {
            'account_name': acc_fields.name,
            'account_number': acc_fields.acc_num,
            'product_number': pn,
        }
