import pika
import os
from dotenv import load_dotenv
import time

load_dotenv()

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    # time.sleep(1) # optional - use to see the queue in action, remove for normal operation

# Connection parameters
connection_params = pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    port=int(os.getenv('RABBITMQ_PORT')),
    credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'))
)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare the queue (same name as the producer)
queue_name = os.getenv('RABBITMQ_QUEUE_TEST')
channel.queue_declare(queue=queue_name)

# Start consuming
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(f' [*] Waiting for messages on queue: {queue_name}. To exit press CTRL+C')

try:
  channel.start_consuming()
except KeyboardInterrupt:
  print("Consumer stopped by user")
  connection.close()