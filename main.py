from flask import Flask
from flask import request as f_request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

TOKEN = '''6274568989:AAEwhaXFHstZ3hP7KFAfJCgrWJ9VpqTLG4s'''
hook_url = "IldamTeam.pythonanywhere.com"
URL = '''https://api.telegram.org/bot{}/'''.format(TOKEN)


def resethook():
    del_web_hook = f'https://api.telegram.org/bot{TOKEN}/deleteWebhook'
    set_web_hook = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={hook_url}'
    print(requests.post(del_web_hook))
    print(requests.post(set_web_hook))


def send_message(chat_id, text, parse_mode='markdown', reply_markup=None):
    url = URL + 'sendMessage'
    if reply_markup:
        anw = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode, 'reply_markup': reply_markup}
    else:
        anw = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    r = requests.post(url, json=anw)
    return r.json()


def delete_message(chat_id, message_id):
    url = URL + 'deleteMessage'
    req = {'chat_id': chat_id, "message_id": message_id}
    r = requests.post(url, json=req)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if f_request.method == 'POST':

        r = f_request.get_json()
        message = r.get('message')

        if message:
            new_chat_member = message.get("new_chat_member")
            new_chat_members = message.get("new_chat_members")
            left_chat_member = message.get("left_chat_member")
            new_chat_photo = message.get("new_chat_photo")

            try:
                chat_id = message['chat']['id']
            except Exception as err:
                print("Chat or ChatId not Found!: \n", err)
                chat_id = None
            if message["text"] == "test":
                send_message(5296922626, "Welcome! ")
            if new_chat_member or new_chat_members or left_chat_member or new_chat_photo:
                # Here deleting message from chat
                delete_message(chat_id, message["message_id"])

            if new_chat_member:
                send_message(chat_id, "Welcome! ")

        return {"ok": True}
    return "<a href='https://t.me/typeHito'><h1>join to channel</h1>"


if __name__ == '__main__':
    send_message(5296922626, "Bot HassBeen started")
    app.run()

