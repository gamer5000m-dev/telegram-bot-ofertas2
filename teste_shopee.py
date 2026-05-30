import asyncio
from playwright.async_api import async_playwright

LINK_TESTE = "https://s.shopee.com.br/5L97hNyYVQ"

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
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("TÍTULO:", await page.title())

        print(
            "TEXTAREAS:",
            await page.locator("textarea").count()
        )

        print(
            "INPUTS:",
            await page.locator("input").count()
        )

        print(
            "BOTOES:",
            await page.locator("button").count()
        )

        try:

            await page.locator(
                "textarea"
            ).first.fill(LINK_TESTE)

            print("LINK PREENCHIDO")

        except Exception as e:

            print("ERRO AO PREENCHER:", e)

        await page.screenshot(
            path="shopee.png",
            full_page=True
        )

        print("SCREENSHOT SALVO")

        await browser.close()

asyncio.run(main())