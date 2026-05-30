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

        print("ABRINDO SHOPEE...")

        await page.goto(
            "https://affiliate.shopee.com.br",
            wait_until="networkidle",
            timeout=60000
        )

        print("URL:", page.url)
        print("TITULO:", await page.title())

        await page.screenshot(
            path="screenshot.png",
            full_page=True
        )

        print("SCREENSHOT SALVO")

        print("CHAT_ID:", CHAT_ID)

        async with aiohttp.ClientSession() as session:

            with open("screenshot.png", "rb") as foto:

                foto_bytes = foto.read()

                data = aiohttp.FormData()

                data.add_field(
                    "chat_id",
                    str(CHAT_ID)
                )

                data.add_field(
                    "photo",
                    foto_bytes,
                    filename="screenshot.png",
                    content_type="image/png"
                )

                resposta = await session.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    data=data
                )

                texto = await resposta.text()

                print("RESPOSTA TELEGRAM:")
                print(texto)

        await browser.close()

asyncio.run(main())