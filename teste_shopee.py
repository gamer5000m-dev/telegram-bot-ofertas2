import os
import asyncio
import aiohttp
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

        await page.goto(
            "https://affiliate.shopee.com.br",
            wait_until="networkidle",
            timeout=60000
        )

        await page.screenshot(
            path="screenshot.png",
            full_page=True
        )

        print("SCREENSHOT SALVO")

        async with aiohttp.ClientSession() as session:

            with open("screenshot.png", "rb") as foto:

                data = aiohttp.FormData()

                data.add_field(
                    "chat_id",
                    CHAT_ID
                )

                data.add_field(
                    "photo",
                    foto,
                    filename="screenshot.png"
                )

                resposta = await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    data=data
                )

                print(await resposta.text())

        await browser.close()

asyncio.run(main())