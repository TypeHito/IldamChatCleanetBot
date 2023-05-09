from flask import Flask
from flask import request as f_request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
# set ssl
sslify = SSLify(app)

# """Global"""
# TOKEN = """5886495741:AAH99PqcvNgD2vzxmtaH3FHVcKzw5ZnmdkQ"""
# hook_url = "https://ildamteam.pythonanywhere.com"

"""Local"""
TOKEN = """5979261876:AAG6mtGYyaxr0UQdmOjDouHTrekgjO_94Hk"""
hook_url = "https://51f4-213-230-82-243.eu.ngrok.io"


URL = f"""https://api.telegram.org/bot{TOKEN}/"""

del_web_hook = f"{URL}deleteWebhook"
set_web_hook = f"{URL}setWebhook?url={hook_url}"

# TypeHito TId = 5754619101
# valids and stats
valid_chats = {}
valid_users = [5754619101]
chat_types = ["group", "supergroup"]
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
    send_message(valid_users[0], f"URL:{hook_url}")
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


def get_valid_chats():
    return "\n".join([str(chat) for chat in valid_chats.keys()])


def get_chat_form(valid_chat):
    chat = valid_chat.get("chat")
    from_ = valid_chat.get("from")
    if chat.get("chat_type") != 'private':
        chat_id = chat.get("id") if chat.get("id") else ''
        chat_type = chat.get("type") if chat.get("type") else ''
        chat_username = chat.get("username") if chat.get("username") else ''
        chat_title = chat.get("title") if chat.get("title") else ''
        chat_msg = f"💬 Chat:  {chat_title}\n" \
                   f"ChatID:  {chat_id}\n" \
                   f"ChatType:  {chat_type}\n" \
                   f"ChatUserName:  {chat_username}\n"
    else:
        chat_msg = ''

    if from_:
        from_id = from_.get("id") if from_.get("id") else ''
        firstname = from_.get("firstname") if from_.get("firstname") else ''
        lastname = from_.get("lastname") if from_.get("lastname") else ''
        username = from_.get("username") if from_.get("username") else ''

        from_msg = f"👤 FromID:  {from_id}\n"\
                   f"FirstName:  {firstname}\n"\
                   f"LastName:  {lastname}\n"\
                   f"UserName:  {username}\n"
    else:
        from_msg = ''
    return chat_msg + from_msg


def get_chats_form():
    text = []
    for i in valid_chats:
       text.append(get_chat_form(valid_chats[i]))
    return text


def admin_message_handler(message):
    chat = message["chat"]
    chat_id = chat["id"]

    text = message['text']

    if text:
        if text[0] == "/":
            if text == "/getchat":
                send_message(chat_id, get_chat_form(valid_chats[chat_id]))
            elif text == "/getchats":
                send_message(chat_id, "\n".join(get_chats_form()))
            elif text == "/savechats":
                send_message(chat_id, valid_chats)

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
                valid_chats[chat_id] = {"from": message['from'], "chat": message["chat"]}
                send_message(valid_users[0], "Please check chats")
                # return {"ok": True}

            if (chat_id in valid_users) or (message["from"]["id"] in valid_users) or ():
                return admin_message_handler(message)

        return {"ok": True}

    return "<a href=\"https://t.me/typeHito\"><h1>Owner</h1>"


if not hook_status:
    reset_hook()
    hook_status = True

if __name__ == "__main__":
    app.run()
