import json
from subprocess import PIPE, run

from playwright.sync_api import sync_playwright


def get_username_password_otp():
    res = run(
        ["op", "item", "get", "Tesla Business Portal", "--format", "json"],
        stdout=PIPE,
        stderr=PIPE,
    )
    blob = json.loads(res.stdout.decode())
    username = blob["fields"][0]["value"]
    password = blob["fields"][1]["value"]
    otp = blob["fields"][3]["totp"]

    return {"username": username, "password": password, "otp": otp}


def order_car():
    credentials = get_username_password_otp()
    print(credentials)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://partners.tesla.com/home/")
        page.get_by_label("Email", exact=True).click()
        page.get_by_label("Email", exact=True).fill(credentials["username"])
        page.get_by_role("button", name="Next").click()
        print("Username filled in")
        page.frame_locator("#sec-cpt-if").locator("#robot-checkbox").check()
        page.frame_locator("#sec-cpt-if").get_by_text("Proceed").click()
        page.get_by_label("password").click()
        page.get_by_label("password").fill(credentials["password"])
        print("Password filled in")

        page.get_by_role("button", name="Sign In").click()
        print("Sign in clicked")
        passcode_input = page.locator('[name="passcode"]')
        passcode_input.wait_for(timeout=0)
        credentials = get_username_password_otp()
        page.get_by_label("passcode").fill(credentials["otp"], timeout=0)
        page.get_by_role("button", name="Submit").click()
        fake_input = page.locator('[name="fake"]')
        fake_input.wait_for(timeout=0)
        # context.close()
        # browser.close()


order_car()
