from flask import Flask
from flask import request as f_request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
# set ssl
sslify = SSLify(app)

"""Global"""
TOKEN = """6240624335:AAFq3tH4ymVtFukVUYLW7-kwZ9VeAIGaNzQ"""
URL = f"""https://api.telegram.org/bot{TOKEN}/"""


# hook_url = "https://ildamteam.pythonanywhere.com"
hook_url = "https://747a-213-230-72-241.ngrok-free.app  "

valid_chats = [5754619101]
valid_users = [5754619101]
rules = ["new_chat_member", "new_chat_members", "left_chat_member", "new_chat_photo", "new_chat_title",
         "delete_chat_photo", "supergroup_chat_created", "pinned_message"]


def reset_hook():
    del_web_hook = f"{URL}deleteWebhook"
    set_web_hook = f"{URL}setWebhook?url={hook_url}"
    send_message(valid_users[0], f"reset bot\n"
                                 f"❌del: {del_web_hook}\n"
                                 f"✅set: {set_web_hook}\n")


def send_message(chat_id, text, parse_mode="markdown"):
    url = URL + "sendMessage"
    req = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    r = requests.post(url, json=req)
    return r.json()


def delete_message(chat_id, message_id):
    url = URL + "deleteMessage"
    req = {"chat_id": chat_id, "message_id": message_id}
    r = requests.post(url, json=req)
    return r.json()


def get_chat_form(valid_chat):
    chat = valid_chat.get("chat")
    chat_id = chat.get("id") if chat.get("id") else ''
    chat_type = chat.get("type") if chat.get("type") else ''
    chat_username = '@' + chat.get("username") if chat.get("username") else ''
    chat_title = chat.get("title") if chat.get("title") else ''

    chat_msg = f"💬 Chat:  {chat_title}\n" \
               f"ChatID:  {chat_id}\n" \
               f"ChatType:  {chat_type}\n" \
               f"ChatUserName:  {chat_username}\n"
    return chat_msg


def admin_message_handler(message):
    chat = message["chat"]
    chat_id = chat["id"]

    text = message['text']

    if text:
        if text[0] == "/":
            if text == "/getchat":
                send_message(chat_id, get_chat_form(message))
            elif text == "/test":
                send_message(chat_id, "test")

    return {"ok": True}


@app.route("/", methods=["POST", "GET"])
def index():
    if f_request.method == "POST":
        r = f_request.get_json()
        message = r.get("message")
        if message:
            try:
                chat_id = message["chat"]["id"]
            except Exception as err:
                send_message(valid_users[0], f" Chat or Chat_ID not Found!: \n{err}\n{r}")
                return {"ok": False}
            try:
                user_id = message["from"]["id"]
            except Exception as err:
                send_message(valid_users[0], f" Chat or Chat_ID not Found!: \n{err}\n{r}")
                return {"ok": False}

            for rule in rules:
                if message.get(rule):
                    delete_message(chat_id, message["message_id"])
                    return {"ok": True}
            if user_id in valid_users:
                return admin_message_handler(message)
            return {"ok": True}
    return "<a href=\"https://t.me/typeHito\"><h1>Owners</h1>"


reset_hook()

if __name__ == "__main__":
    app.run()
