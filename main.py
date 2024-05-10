import json
from playwright.sync_api import sync_playwright
from subprocess import run, PIPE


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


def order_car():
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50, headless=False)
        page = browser.new_page()
        page.goto(
            "https://auth.tesla.com/oauth2/v1/authorize?response_type=code&client_id=teslaforbusiness-prod&redirect_uri=https%3A%2F%2Fwww.tesla.com%2Fteslaaccount%2Fbusiness%2Ffulfillment%2Foauth2-connect&scope=email+profile+openid+offline_access&state=4mxCQokkKEr8wCI5pKzetp4wF9RlTxcM"
        )
        page.screenshot(path="example.png")
        browser.close()

order_car()
