import pika
import pickle


with open('myfile.pkl', 'rb') as file:
    model = pickle.load(file)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='features')
channel.queue_declare(queue='y_pred')


def callback(ch, method, properties, body):
    message = pickle.loads(body)
    features = message['body']
    message_id = message['id']

    prediction = model.predict([features])[0]

    y_pred_message = {
        'id': message_id,
        'body': prediction
    }
    channel.basic_publish(exchange='', routing_key='y_pred', body=pickle.dumps(y_pred_message))
    print(f"Предсказание отправлено для id: {message_id}")


channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)

print('Ожидание сообщений...')
channel.start_consuming()
