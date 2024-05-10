import json
from subprocess import PIPE, run


def get_username_password_otp():
    res = run(
        ["op", "item", "get", "Tesla Business Portal", "--format", "json"],
        stdout=PIPE,
        stderr=PIPE,
    )
    blob = json.loads(res.stdout.decode())
    username = blob["fields"][0]["value"]
    password = blob["fields"][1]["value"]
    otp = blob["fields"][3]["value"]

    return {"username": username, "password": password, "otp": otp}


get_username_password_otp()
