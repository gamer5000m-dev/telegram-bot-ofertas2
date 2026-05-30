import os
import asyncio
from playwright.async_api import async_playwright

SHOPEE_EMAIL = os.getenv("SHOPEE_EMAIL")
SHOPEE_SENHA = os.getenv("SHOPEE_SENHA")

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = await browser.new_page()

        print("ABRINDO LOGIN...")

        await page.goto(
            "https://affiliate.shopee.com.br/login",
            wait_until="networkidle",
            timeout=60000
        )

        print("URL:", page.url)
        print("TITULO:", await page.title())

        print("INPUTS:", await page.locator("input").count())
        print("BOTOES:", await page.locator("button").count())

        await page.screenshot(
            path="login.png",
            full_page=True
        )

        print("SCREENSHOT LOGIN SALVO")

        await browser.close()

asyncio.run(main())