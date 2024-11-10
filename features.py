import time
import random
import pickle
import pika
from sklearn.datasets import load_diabetes
from datetime import datetime

data = load_diabetes()
X, y = data.data, data.target

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='features')
channel.queue_declare(queue='y_true')

while True:
    random_row = random.randint(0, len(y) - 1)
    message_id = datetime.timestamp(datetime.now())

    message_y_true = {
        'id': message_id,
        'body': y[random_row]
    }
    message_features = {
        'id': message_id,
        'body': X[random_row].tolist()
    }

    channel.basic_publish(exchange='', routing_key='y_true', body=pickle.dumps(message_y_true))
    channel.basic_publish(exchange='', routing_key='features', body=pickle.dumps(message_features))

    print(f"Отправлено сообщение: {message_id}")
    time.sleep(10)
