import time

from playwright.sync_api import sync_playwright

from auth import get_credentials
from options import get_car_order


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
    credentials = get_credentials()
    order = get_car_order(
        model, spec, colour, interior, wheels, tow_hitch, enhanced, self_driving
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tesla.com/teslaaccount/business/orders/")

        # Login

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
        credentials = get_credentials()
        page.get_by_label("passcode").click(timeout=60000)
        page.get_by_label("passcode").fill(credentials["otp"])
        page.get_by_role("button", name="Submit").click()

        # Select account

        page.get_by_label("Select an Account").click()
        page.get_by_label("", exact=True).get_by_text(
            "Octopus Electric Vehicles"
        ).click()
        page.get_by_role("button", name="Continue").click()

        # Create order

        page.get_by_role("button", name="Create Order").click()

        # Select model
        
        page.get_by_text(order["model"], exact=True).click()

        page.get_by_role("button", name="Accept").click()
        page.get_by_role("button", name="Next").click()
        page.mouse.wheel(0, 250)

        # Select spec

        page.get_by_text(order["spec"], exact=True).click()
        page.mouse.wheel(0, 250)

        # Select colour

        page.get_by_role("img", name=order["colour"], exact=True).locator("image").click()
        page.mouse.wheel(0, 500)

        # Select wheels

        page.get_by_role("img", name=order["wheels"]).locator("image").click()

        # Select options

        if order["tow_hitch"]:
            page.get_by_label("Select Option - Tow Hitch - £" ).click()
        if order["enhanced"]:
            page.get_by_label("Select Option - Enhanced" ).click()
        elif order["self_driving"]:
            page.get_by_label("Select Option - Full Self-").click()

        # Select interior

        page.get_by_role("img", name=order["interior"], exact=True).locator("image").click()

        # Complete order

        page.mouse.wheel(0, 2000)
        page.get_by_role("button", name="Add to Order", exact=True).click(timeout=10000000)

        # Finish

        time.sleep(60000)
        context.close()
        browser.close()


# order_car(
#     model="Model 3",
#     colour="Stealth Grey",
#     interior="black",
#     spec="long range",
#     wheels='19" Nova alloy wheels',
#     tow_hitch=True,
#     enhanced=False,
#     self_driving=True,
# )

order_car(
    model="Model Y",
    colour="Deep Blue Metallic",
    interior="black and white",
    spec="rear wheel drive",
    wheels='20" Induction alloy wheels',
    tow_hitch=False,
    enhanced=True,
    self_driving=False,
)
