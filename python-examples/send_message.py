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

# message to send
message = "{'destinatary': 'mail@gmail.com'}"

# basic publish to our named exchange
# fanout type ignores routing_key so we leave it blank
channel.basic_publish(exchange='logs', routing_key='', body=message)

# print after publish is finished
print(" [x] Sent {}".format(message))

# closing connection
connection.close()
