import json
import time
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


def order_car(
    model,
    spec,
    colour,
    interior,
    wheels,
    tow_hitch=False,
    enhanced=False,
    self_driving=False,
):
    credentials = get_username_password_otp()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tesla.com/teslaaccount/business/orders/")

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
        page.get_by_label("passcode").click(timeout=60000)
        page.get_by_label("passcode").fill(credentials["otp"])
        page.get_by_role("button", name="Submit").click()
        page.get_by_label("Select an Account").click()
        page.get_by_label("", exact=True).get_by_text(
            "Octopus Electric Vehicles"
        ).click()
        page.get_by_role("button", name="Continue").click()
        page.get_by_role("button", name="Create Order").click()
        if model == "Model 3":
            page.get_by_text("Model 3").click()
        elif model == "Model Y":
            page.get_by_text("Model Y").click()
        page.get_by_role("button", name="Accept").click()
        page.get_by_role("button", name="Next").click()
        page.mouse.wheel(0, 250)
        if spec == "rear wheel drive":
            page.get_by_text("Rear-Wheel Drive", exact=True).click()
        elif spec == "long range":
            page.get_by_text("Long Range All-Wheel Drive").click()
        elif spec == "performance":
            page.get_by_text("Performance All-Wheel Drive").click()
        page.mouse.wheel(0, 250)
        if colour == "Pearl White Multi-Coat":
            page.get_by_role("img", name="Pearl White Multi-Coat").locator(
                "image"
            ).click()
        elif colour == "Deep Blue Metallic":
            page.get_by_role("img", name="Deep Blue Metallic").locator("image").click()
        elif colour == "Solid Black":
            page.get_by_role("img", name="Solid Black").locator("image").click()
        elif colour == "Ultra Red":
            page.get_by_role("img", name="Ultra Red").locator("image").click()
        elif colour == "Stealth Grey":
            page.get_by_role("img", name="Stealth Grey").locator("image").click()
        elif colour == "Quicksilver":
            page.get_by_role("img", name="Quicksilver").locator("image").click()
        page.mouse.wheel(0, 500)

        if wheels == '20" Induction alloy wheels':
            page.get_by_role("img", name="’’ Induction Wheels").locator("image").click()
        elif wheels == '19" Gemini alloy wheels':
            page.get_by_role("img", name="’’ Gemini Wheels").locator("image").click()
        elif wheels == '18" Photon alloy wheels':
            page.get_by_role("img", name="’’ Photon Wheels").locator("image").click()
        elif wheels == '19" Nova alloy wheels':
            page.get_by_role("img", name="’’ Nova Wheels").locator("image").click()

        if tow_hitch:
            page.get_by_label("Select Option - Tow Hitch - £").click()

        if enhanced:
            page.get_by_label("Select Option - Enhanced").click()
        elif self_driving:
            page.get_by_label("Select Option - Full Self-").click()

        if interior == "black":
            page.get_by_role("img", name="Black", exact=True).locator("image").click()
        elif interior == "black and white":
            page.get_by_role("img", name="Black and White").locator("image").click()
        elif interior == "All Black":
            page.get_by_role("img", name="All Black").locator("image").click()
        page.mouse.wheel(0, 2000)
        page.get_by_role("button", name="Add to Order").click(timeout=10000000)
        time.sleep(60000)
        context.close()
        browser.close()


order_car(
    model="Model 3",
    colour="Stealth Grey",
    interior="black",
    spec="rear wheel drive",
    wheels='19" Nova alloy wheels',
    tow_hitch=True,
    enhanced=False,
    self_driving=True,
)
