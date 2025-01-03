import pika
import os
from dotenv import load_dotenv

load_dotenv()

# Connection parameters (replace with your NodePort)
connection_params = pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    port=int(os.getenv('RABBITMQ_PORT')),
    credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'))
)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Create queue
channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE_TEST'))

# Send message
message = 'Hello, RabbitMQ4'
channel.basic_publish(exchange='', routing_key='hello', body=message)
print(f" [x] Sent: {message}")

connection.close()
