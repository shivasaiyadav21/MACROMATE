import requests
import streamlit as st


def get_telegram_chat_id():

    token = st.secrets["TELEGRAM_BOT_TOKEN"]

    url = f"https://api.telegram.org/bot{token}/getUpdates"

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    if not data.get("ok"):
        return None

    updates = data.get("result", [])

    if not updates:
        return None

    # Get the latest message
    latest_update = updates[-1]

    message = latest_update.get("message")

    if not message:
        return None

    chat = message.get("chat")

    if not chat:
        return None

    return chat.get("id")


def send_telegram_message(chat_id, message):

    token = st.secrets["TELEGRAM_BOT_TOKEN"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(
        url,
        data=data,
        timeout=10
    )

    return response.json()