from flask import Flask
from flask import request as f_request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
# set ssl
sslify = SSLify(app)

# """Global"""
# TOKEN = """6274568989:AAHDBHET1_VnepsrmFl0LqZmBqTDbgoH7xw"""
# hook_url = "IldamTeam.pythonanywhere.com"

"""Local"""
TOKEN = """5979261876:AAG6mtGYyaxr0UQdmOjDouHTrekgjO_94Hk"""
hook_url = "https://f094-213-230-82-243.eu.ngrok.io"


URL = f"""https://api.telegram.org/bot{TOKEN}/"""

del_web_hook = f"{URL}deleteWebhook"
set_web_hook = f"{URL}setWebhook?url={hook_url}"

# TypeHito TId = 5754619101
# valids and stats
valid_chats = {5296922626: {}, -962923652: {}, 5754619101: {}}
valid_users = [5754619101]
hook_status = False

rules = ["new_chat_member", "new_chat_members", "left_chat_member", "new_chat_photo", "new_chat_title",
         "delete_chat_photo", "supergroup_chat_created", "pinned_message"]

msg = {
    "check": "✅",
    "uncheck": "❌"
}


def reset_hook():
    del_hook_status = requests.post(del_web_hook).status_code
    set_hook_status = requests.post(set_web_hook).status_code
    send_message(valid_users[0],
                 f"\n{msg['check']  if del_hook_status == 200 else msg['uncheck']} HookDel status: {del_hook_status}"
                 f"\n{msg['check']  if set_hook_status == 200 else msg['uncheck']} HookSet status: {set_hook_status}")


def send_message(chat_id, text, parse_mode="markdown", reply_markup=None):
    url = URL + "sendMessage"
    if reply_markup:
        req = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "reply_markup": reply_markup}
    else:
        req = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    r = requests.post(url, json=req)
    return r.json()


def delete_message(chat_id, message_id):
    url = URL + "deleteMessage"
    req = {"chat_id": chat_id, "message_id": message_id}
    r = requests.post(url, json=req)
    return r.json()


def admin_message_handler(message):
    chat = message["chat"]
    chat_id = chat["id"]
    chat_type = chat["type"]
    chat_title = chat["title"] if chat_type == "group" else chat_type

    # from_ = message["from"]
    # from_id = from_["id"]
    # first_name = from_["username"]

    text = message['text']
    message_id = message['message_id']

    if text:
        if text[0] == "/":
            command, value = str(text).split(" ")
            if command == "/getchat":
                if chat_type == "group":
                    send_message(
                        chat_id,
                        f"💬Chat ::  {chat_title} ::\n"
                        f"🆔infoChatID:  {chat_id}\n"
                        f"✉️ MessageID:  {message_id}")
                else: pass
            elif command == "/getchats":


            send_message(chat_id, f"command is: {command}\nValues is: {value}")

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

            for rule in rules:
                if message.get(rule):
                    # Here deleting message from chat
                    delete_message(chat_id, message["message_id"])
                    return {"ok": True}

            if chat_id not in valid_chats:
                valid_chats[chat_id] = {}
                send_message(valid_users[0], str(valid_chats))
                return {"ok": True}

            if (chat_id in valid_users) or (message["from"]["id"] in valid_users):
                return admin_message_handler(message)

        return {"ok": True}

    return "<a href=\"https://t.me/typeHito\"><h1>Owner</h1>"


if not hook_status:
    reset_hook()
    hook_status = True

if __name__ == "__main__":
    send_message(valid_users[0], "Bot HasBeen started")
    app.run()
