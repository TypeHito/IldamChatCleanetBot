from flask import Flask
from flask import request as f_request
import requests
from flask_sslify import SSLify

app = Flask(__name__)
# set ssl
sslify = SSLify(app)

# """Global"""
# TOKEN = """6274568989:AAEwhaXFHstZ3hP7KFAfJCgrWJ9VpqTLG4s"""
# hook_url = "IldamTeam.pythonanywhere.com"

"""Local"""
TOKEN = """6274568989:AAEwhaXFHstZ3hP7KFAfJCgrWJ9VpqTLG4s"""
hook_url = "https://e302-213-230-82-243.eu.ngrok.io"

# TypeHito TId = 5296922626
admin = 5296922626
URL = """https://api.telegram.org/bot{}/""".format(TOKEN)
hook_status = False

rules = ["new_chat_member", "new_chat_members", "left_chat_member", "new_chat_photo", "new_chat_title",
         "delete_chat_photo", "supergroup_chat_created"]


def reset_hook():
    del_web_hook = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    set_web_hook = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={hook_url}"
    del_hook_status = requests.post(del_web_hook)
    set_hook_status = requests.post(set_web_hook)
    send_message(admin, f"Hook del status: {del_hook_status}\nHook set status: {set_hook_status}")


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


@app.route("/", methods=["POST", "GET"])
def index():
    if f_request.method == "POST":

        r = f_request.get_json()
        message = r.get("message")

        if message:
            try:
                chat_id = message["chat"]["id"]
            except Exception as err:
                send_message(admin, f"Chat or ChatId not Found!: \n{err}\n{r}")
                chat_id = None

            for rule in rules:
                if message.get(rule):
                    # Here deleting message from chat
                    delete_message(chat_id, message["message_id"])

            if message.get("new_chat_member"):
                send_message(chat_id, f"""Welcome! {message.get(message["from"]["username"])}""")
                return {"ok": True}

            if message.get("text") == "test":
                print(send_message(admin, "Test Finished"))
                return {"ok": True}
        return {"ok": True}
    return "<a href=\"https://t.me/typeHito\"><h1>Owner</h1>"


if not hook_status:
    reset_hook()
    hook_status = True

if __name__ == "__main__":
    send_message(5296922626, "Bot HasBeen started")
    app.run()
