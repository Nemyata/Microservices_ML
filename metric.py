import pika
import pickle
import csv

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='y_true')
channel.queue_declare(queue='y_pred')

y_true_dict = {}
y_pred_dict = {}


def calculate_absolute_error(y_true, y_pred):
    return abs(y_true - y_pred)


def handle_message(y_true_id):
    if y_true_id in y_true_dict and y_true_id in y_pred_dict:
        y_true = y_true_dict.pop(y_true_id)
        y_pred = y_pred_dict.pop(y_true_id)
        absolute_error = calculate_absolute_error(y_true, y_pred)
        print(f"Записываю в файл: {y_true_id}, {y_true}, {y_pred}, {absolute_error}")

        with open('./logs/metric_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([y_true_id, y_true, y_pred, absolute_error])
    else:
        print(f"Не хватает данных для id: {y_true_id}")


def callback_y_true(ch, method, properties, body):
    message = pickle.loads(body)
    y_true_dict[message['id']] = message['body']
    handle_message(message['id'])

def callback_y_pred(ch, method, properties, body):
    message = pickle.loads(body)
    y_pred_dict[message['id']] = message['body']
    handle_message(message['id'])


channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)

print("Ожидание сообщений...")
channel.start_consuming()
