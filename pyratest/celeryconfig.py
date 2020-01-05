
broker_url = 'amqp://127.0.0.1:5672'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/London'
enable_utc = True

imports = ('pyratest.tasks.orders_report',
                  )
