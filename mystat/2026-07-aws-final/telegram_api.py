import json
import logging
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


def call(token, method, data):
    request = Request(f"https://api.telegram.org/bot{token}/{method}", json.dumps(data).encode(),
                      {"Content-Type": "application/json"})
    with urlopen(request, timeout=35) as response:
        result = json.load(response)
    if not result.get("ok"):
        raise RuntimeError("Telegram API error")
    return result["result"]


def poll(token, handler):
    offset = 0
    while True:
        try:
            for update in call(token, "getUpdates", {"offset": offset, "timeout": 25, "allowed_updates": ["message"]}):
                message = update.get("message")
                if message and message.get("text", "").strip() and "from" in message:
                    text = handler(message)
                    call(token, "sendMessage", {"chat_id": message["chat"]["id"], "text": text})
                offset = update["update_id"] + 1
        except (URLError, OSError, RuntimeError, ValueError) as error:
            logging.warning("Retry after %s", type(error).__name__)
            time.sleep(3)
