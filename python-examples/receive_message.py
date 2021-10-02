# encoding=utf8

import pika

# ConnectionsParameters receive credentials as an instance of PlanCredentials
# https://pika.readthedocs.io/en/stable/modules/credentials.html
credentials = pika.credentials.PlainCredentials("username", "password", False)

# connecting to RabbitMQ on localhost:8888
# (check https://github.com/pqzada/python-rabbitmq/blob/main/docker-compose.yaml)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=8888, credentials=credentials))

# create channel
channel = connection.channel()

# producer can only send messages from exchange. Exchange receives messages from producers and pushes them into queues
# `fanout` type broadcasts all the messages it receives to all the queues it knows
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# empty queue name declared so server choose a random name for us. Secondly once the consumer connection is closed,
# the queue should be deleted thanks to flag `exclusive=True`
result = channel.queue_declare(queue='', exclusive=True)

# getting queue name
queue_name = result.method.queue

# here we tell the exhcange to send messages to our queue
channel.queue_bind(exchange='logs', queue=queue_name)

# info message
print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    """
    Each time we receive a message, this callback function will be call by pika library.
    In this case, callback function prints message body
    """
    print(" [x] {}".format(body))


# notify to RabbitMQ that `callback` function receive messages from `queue_name` queue
# message ack is automatic (auto_ack=True). In case of manual ack, delete this flag and
# add manual ack in callback (https://www.rabbitmq.com/tutorials/tutorial-two-python.html)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# infinite loop that waits for messages and call callback function
channel.start_consuming()
