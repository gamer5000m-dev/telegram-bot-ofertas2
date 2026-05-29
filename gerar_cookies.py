from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto(
        "https://affiliate.shopee.com.br/login"
    )

    print("")
    print("FAÇA LOGIN MANUALMENTE 🔥")
    print("")

    input("Depois do login aperta ENTER 🔥")

    context.storage_state(
        path="shopee_state.json"
    )

    print("")
    print("COOKIES SALVOS 🔥")
    print("")

    browser.close()