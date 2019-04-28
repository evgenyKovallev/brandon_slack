import pika
from brandon_slack import settings

connection = pika.BlockingConnection(pika.ConnectionParameters(
               settings.BROKER_HOST))
channel = connection.channel()
channel.queue_declare(queue='slack')
