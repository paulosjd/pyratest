def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('notifier', '/notifier')
    config.add_route('order_info', '/order-info')
    config.add_route('account_task', '/account-task')
    config.add_route('account_info', '/account-info')
    config.add_route('account_orders', '/account-orders')
    config.add_route('acc_name_and_product', '/account-name-product')
