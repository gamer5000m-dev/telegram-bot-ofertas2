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


# GERAR LINK AFILIADO ML
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

            print("ABRIU PAGINA")

            await page.wait_for_timeout(5000)

            # PREENCHE INPUT
            await page.locator(
                "input"
            ).first.fill(link_produto)

            print("LINK PREENCHIDO")

            await page.wait_for_timeout(2000)

            # PROCURA BOTÃO
            botoes = await page.locator(
                "button"
            ).all()

            for botao in botoes:

                try:

                    texto_botao = await botao.inner_text()

                    print("BOTAO:", texto_botao)

                    if (
                        "Gerar" in texto_botao
                        or "Criar" in texto_botao
                    ):

                        await botao.click()

                        print("CLICOU GERAR")

                        break

                except:
                    pass

            await page.wait_for_timeout(7000)

            # PEGA HTML
            html = await page.content()

            # DEBUG
            print(html[:5000])

            # PROCURA LINK SOCIAL
            links_social = re.findall(
                r'https://www\.mercadolivre\.com\.br/social/\S+',
                html
            )

            if links_social:

                novo_link = links_social[0]

                print("LINK GERADO:", novo_link)

                await browser.close()

                return novo_link

            await browser.close()

            return link_produto

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