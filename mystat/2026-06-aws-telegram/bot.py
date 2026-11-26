import json
import logging
import os
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


def api(token, method, fields):
    request = Request(f"https://api.telegram.org/bot{token}/{method}",
                      json.dumps(fields).encode(), {"Content-Type": "application/json"})
    with urlopen(request, timeout=35) as response:
        result = json.load(response)
    if not result.get("ok"):
        raise RuntimeError("Telegram returned an API error")
    return result["result"]


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    offset = 0
    print("Telegram bot started", flush=True)
    while True:
        try:
            updates = api(token, "getUpdates", {"offset": offset, "timeout": 25, "allowed_updates": ["message"]})
            for update in updates:
                message = update.get("message", {})
                if "text" in message:
                    text = message["text"]
                    reply = "Привіт! Команда /help покаже можливості." if text.strip().split("@", 1)[0].partition(" ")[0] == "/start" else "Напишіть /start, щоб перевірити зв’язок."
                    api(token, "sendMessage", {"chat_id": message["chat"]["id"], "text": reply})
                offset = update["update_id"] + 1
        except (URLError, ValueError, OSError, RuntimeError) as error:
            logging.warning("Telegram operation failed (%s); retrying", type(error).__name__)
            time.sleep(3)


if __name__ == "__main__":
    main()
