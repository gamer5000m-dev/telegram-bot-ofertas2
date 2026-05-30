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

        print(
            "EMAIL DIGITADO:",
            await email.input_value()
        )

        print(
            "SENHA TAMANHO:",
            len(await senha.input_value())
        )

        print("EMAIL E SENHA PREENCHIDOS")

        botoes = page.locator("button")

        total = await botoes.count()

        print("TOTAL BOTOES:", total)

        for i in range(total):

            try:

                texto = await botoes.nth(i).inner_text()

                print(f"BOTAO {i}: {texto}")

            except:
                pass

        print("CLICANDO EM ENTRAR...")

        await botoes.nth(2).click(force=True)

        await page.wait_for_timeout(10000)

        print("URL APÓS LOGIN:", page.url)

        print(
            "TÍTULO APÓS LOGIN:",
            await page.title()
        )

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

        print("\n====================")
        print("TEXTO DA PAGINA")
        print("====================\n")

        try:

            texto_pagina = await page.locator(
                "body"
            ).inner_text()

            print(texto_pagina)

        except Exception as e:

            print("ERRO AO LER PAGINA:", e)

        await page.screenshot(
            path="depois_login.png",
            full_page=True
        )

        print("SCREENSHOT SALVO")

        await browser.close()

asyncio.run(main())