from telethon import TelegramClient, events
from playwright.async_api import async_playwright
import os
import re

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# CANAL DESTINO
canal_destino = -1003914285353

# CANAIS MONITORADOS
canais_monitorados = [
    -1001353489373
]

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

# LOGIN
client.start(
    phone="+5561994348181",
    code_callback=lambda: "82195"
)

print("BOT ONLINE 🔥")


# GERADOR LINK AFILIADO ML
async def gerar_link_afiliado_ml(link_produto):

    try:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            await page.goto(
                "https://www.mercadolivre.com.br/afiliados/linkbuilder",
                timeout=60000
            )

            await page.wait_for_timeout(3000)

            # CAMPO TEXTAREA
            await page.fill(
                "textarea",
                link_produto
            )

            await page.wait_for_timeout(1000)

            # BOTÃO GERAR
            await page.click("button")

            await page.wait_for_timeout(5000)

            # PEGA TODOS INPUTS
            inputs = await page.locator("input").all()

            novo_link = link_produto

            for i in inputs:

                try:

                    valor = await i.input_value()

                    if (
                        "mercadolivre.com.br/social/" in valor
                    ):

                        novo_link = valor
                        break

                except:
                    pass

            await browser.close()

            print("LINK ORIGINAL:", link_produto)
            print("NOVO LINK:", novo_link)

            return novo_link

    except Exception as e:

        print("ERRO AFILIADO:", e)

        return link_produto


@client.on(events.NewMessage(chats=canais_monitorados))
async def handler(event):

    try:

        texto = event.raw_text

        if not texto:
            return

        # REMOVE MARCA D'ÁGUA
        texto = re.sub(
            r"📍.*",
            "",
            texto
        ).strip()

        # PEGA LINKS
        links = re.findall(
            r'https?://\S+',
            texto
        )

        # PROCESSA LINKS
        for link in links:

            # MERCADO LIVRE
            if (
                "mercadolivre" in link.lower()
                or "meli.la" in link.lower()
            ):

                novo_link = await gerar_link_afiliado_ml(link)

                texto = texto.replace(
                    link,
                    novo_link
                )

        # ENVIA FOTO + TEXTO
        if event.photo:

            arquivo = await event.download_media()

            await client.send_file(
                canal_destino,
                arquivo,
                caption=texto,
                link_preview=False
            )

        else:

            await client.send_message(
                canal_destino,
                texto,
                link_preview=True
            )

        print("Oferta enviada 🔥")

    except Exception as e:

        print("ERRO:", e)


client.run_until_disconnected()