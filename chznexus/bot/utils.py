import re
import urllib.parse


def double_url_encode(message: str) -> str:
    return urllib.parse.quote(urllib.parse.quote(message))


def parse_login_ok(message):
    match = re.search(r"y4:(\w+)", message)
    return match.group(1) if match else None


def spoof_login_ok_response(message):
    message = message.replace("y11:is_visiteurt", "y11:is_visiteurf")
    if "y2:idi" not in message:
        message = message.replace("goy4:pets", "y2:idi999999goy4:pets")
    if "y2:xpi" not in message:
        message = message.replace("y2:xpi", "y2:xpi12345")
    print("🎭 Modified LOGIN_OK to spoof visitor flag.")
    return message
