from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)

MESSAGES_FILENAME = 'messages_file.json'

def load_messages():
    with open(MESSAGES_FILENAME, 'r') as messages_file:
        data = json.load(messages_file)
        return data['messages']

all_messages = load_messages()  # Список всех сообщений

def save_messages():
    with open(MESSAGES_FILENAME, 'w') as messages_file:
        data = {
            'messages': all_messages,
        }
        json.dump(data, messages_file)

# Функция добавления нового сообщения
# Пример: add_message("Вася", "Оставьте мне пивка плз")
def add_message(sender, text):
  # <= начинается с отступа код внутри функции этой
  # Создавать новое сообщение (новую структуру - словарь)
  new_message = {
      "text": text,
      "sender": sender,
      "time": datetime.now().strftime("%H:%M:%S"),
  }
  # Добавлять сообщение в список
  all_messages.append(new_message)
  for message in all_messages:
      message['text'] = filter_text(message['text'])
      message['sender'] = filter_name(message['sender'])




# Функция вывода всех сообщений
def print_all():
  for msg in all_messages:
    print(f'[{msg["sender"]}]: {msg["text"]} / {msg["time"]}')

# Пример вызова функции без параметров
print_all()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/get_messages')
def get_messages():
    return {'messages': all_messages}

def filter_text(text):
    if 1000 < len(text) < 2:
        return "[FILTERED]"
    else:
        return text


def filter_name(name):
    if 100 < len(name) < 3:
        return "[FILTERED]"
    else:
        return name

@app.route('/send_message')
def send_message():
    text = filter_text(request.args["text"])
    name = filter_name(request.args["sender"])
    add_message(name, text)
    return 'ok'

@app.route('/chat')
def chat():
    return render_template("form.html")


if __name__ == '__main__':
    app.run()
