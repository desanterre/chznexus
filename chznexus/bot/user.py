import os

import pandas as pd

from chznexus.bin.config import EXCEL_FILENAME

user_map = {}


def append_to_excel(user_id, username, filename=None):
    if filename is None:
        filename = EXCEL_FILENAME

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["User ID", "Username"])

    if user_id in df["User ID"].values:
        return

    new_data = pd.DataFrame({"User ID": [user_id], "Username": [username]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(filename, index=False)
    print(f"✅ User {user_id} ({username}) logged in")


def update_user_map(user_id, username):
    user_map[user_id] = username
