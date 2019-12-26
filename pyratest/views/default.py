from pyramid.view import view_config
from sqlalchemy import exc

from .. import models


@view_config(route_name='home', renderer='../templates/mytemplate.mako')
def my_view(request):
    query = request.dbsession.query(models.Order)
    one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': one, 'project': 'pyratest'}


class OrderInfoView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='../templates/mytemplate.mako')
    def get_order_info(self, request):
        try:
            order = self.request.dbsession.query(models.Order).filter(
                models.Order.order_id == request.params.order_id).one()
        except exc.SQLAlchemyError:
            return {'status': 'order not found'}

        try:
            product_id = self.request.dbsession.query(models.Product.id).filter(
                models.Product.product_id == request.params.product_number).one()[0]
        except exc.SQLAlchemyError:
            return {'status': 'product not_found'}

        try:
            acc_name = self.request.dbsession.query(models.Account.name).filter(
                models.Account.number == request.params.account_number).one()[0]
        except exc.SQLAlchemyError:
            return {'status': 'account not found'}

        return {'order_number': order.number, 'product_id': product_id, 'account_name': acc_name}
