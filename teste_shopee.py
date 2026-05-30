import os
import asyncio
import aiohttp
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

        print("CLICANDO EM ENTRAR...")

        await page.locator(
            'button:has-text("Entrar")'
        ).click(force=True)

        await page.wait_for_timeout(15000)

        print("URL APOS LOGIN:", page.url)
        print("TITULO APOS LOGIN:", await page.title())

        try:
            texto = await page.locator("body").inner_text()

            print("===== TEXTO DA PAGINA =====")
            print(texto[:5000])

            if "senha incorreta" in texto.lower():
                print("SENHA INCORRETA")

            if "captcha" in texto.lower():
                print("CAPTCHA DETECTADO")

            if "verificação" in texto.lower():
                print("VERIFICACAO DETECTADA")

            if "sms" in texto.lower():
                print("SMS DETECTADO")

        except Exception as e:
            print("ERRO AO LER PAGINA:", e)

        await page.screenshot(
            path="screenshot.png",
            full_page=True
        )

        print("SCREENSHOT SALVA")

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

                print("STATUS:", resposta.status)

                print(
                    "RESPOSTA TELEGRAM:",
                    await resposta.text()
                )

        await browser.close()


asyncio.run(main())