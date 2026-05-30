import os
import asyncio
import aiohttp
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SHOPEE_EMAIL = os.getenv("SHOPEE_EMAIL")
SHOPEE_SENHA = os.getenv("SHOPEE_SENHA")


async def enviar_arquivo(caminho, legenda):

    async with aiohttp.ClientSession() as session:

        with open(caminho, "rb") as arquivo:

            data = aiohttp.FormData()

            data.add_field(
                "chat_id",
                str(CHAT_ID)
            )

            data.add_field(
                "document",
                arquivo.read(),
                filename=os.path.basename(caminho),
                content_type="application/octet-stream"
            )

            resposta = await session.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                data=data
            )

            print("TELEGRAM:")
            print(await resposta.text())


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
            "https://shopee.com.br/buyer/login?next=https://affiliate.shopee.com.br/login",
            wait_until="networkidle",
            timeout=60000
        )

        print("URL:", page.url)
        print("TITULO:", await page.title())

        try:

            await page.get_by_text(
                "Aceitar todos os cookies",
                exact=False
            ).click(timeout=5000)

            print("COOKIES ACEITOS")

            await page.wait_for_timeout(2000)

        except:

            print("SEM POPUP DE COOKIES")

        email = page.locator("input").nth(0)
        senha = page.locator("input").nth(1)

        await email.fill(SHOPEE_EMAIL)
        await senha.fill(SHOPEE_SENHA)

        print("EMAIL E SENHA PREENCHIDOS")

        await page.locator("button").filter(
            has_text="Entrar"
        ).first.click(force=True)

        print("CLICOU EM ENTRAR")

        await page.wait_for_timeout(15000)

        print("URL APOS LOGIN:", page.url)
        print("TITULO APOS LOGIN:", await page.title())

        try:

            texto = await page.locator("body").inner_text()

            print("===== TEXTO DA PAGINA =====")
            print(texto[:5000])

        except Exception as e:

            print("ERRO TEXTO:", e)

        try:

            html = await page.content()

            with open(
                "pagina.html",
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html)

            print("HTML SALVO")

        except Exception as e:

            print("ERRO HTML:", e)

        await page.screenshot(
            path="screenshot.png",
            full_page=True
        )

        print("SCREENSHOT SALVA")

        await enviar_arquivo(
            "screenshot.png",
            "Screenshot Shopee"
        )

        await enviar_arquivo(
            "pagina.html",
            "HTML Shopee"
        )

        await browser.close()


asyncio.run(main())