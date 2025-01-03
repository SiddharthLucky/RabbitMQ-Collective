import pika
import time
import os
from dotenv import load_dotenv

load_dotenv()

def wait_for_rabbitmq_connection(connection_params):
    """Waits for a RabbitMQ connection to be available."""
    while True:
        try:
            connection = pika.BlockingConnection(connection_params)
            if connection.is_open:
                connection.close()
                return
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ connection...")
            time.sleep(5)


def setup_rabbitmq():
    """Sets up RabbitMQ exchanges, queues, and bindings."""
    # Connection parameters
    credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'))
    connection_params = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)), # Default port if not set
        credentials=credentials
    )

    # Wait for connection
    wait_for_rabbitmq_connection(connection_params)

    # Establish connection and channel
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Define exchange, queues, and bindings
    exchange_name = os.getenv('RABBITMQ_QUOTEGEN_EXCHANGE_NAME')
    queues_bindings = [
        {'queue': os.getenv('RABBITMQ_QUEUE_TOPIC_FINDER'), 'routing_key': os.getenv('RABBITMQ_ROUTING_KEY_QUOTE_FINDER')},
        {'queue': os.getenv('RABBITMQ_QUEUE_TOPIC_INITIAL'), 'routing_key': os.getenv('RABBITMQ_ROUTING_KEY_TOPIC_INITIAL')},
        {'queue': os.getenv('RABBITMQ_QUEUE_FILTER_LEVEL1'), 'routing_key': os.getenv('RABBITMQ_ROUTING_KEY_FILTER_LEVEL1')},
    ]

    # Create Exchange (idempotently)
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

    # Create queues and bindings
    for item in queues_bindings:
        queue_name = item['queue']
        routing_key = item['routing_key']

        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    print("RabbitMQ setup completed.")
    connection.close()


if __name__ == "__main__":
    setup_rabbitmq()
