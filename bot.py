import aiohttp
from telethon import TelegramClient, events
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
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
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            page = await browser.new_page()

            # STEALTH
            await Stealth().apply_stealth_async(page)

            await page.goto(
                "https://www.mercadolivre.com.br/afiliados/linkbuilder",
                timeout=60000
            )

            print("ABRIU PAGINA")

            await page.wait_for_timeout(7000)

            # PEGA TODOS INPUTS
            inputs = await page.locator(
                "input"
            ).all()

            achou_input = False

            # PROCURA INPUT TYPE TEXT
            for campo in inputs:

                try:

                    tipo = await campo.get_attribute(
                        "type"
                    )

                    print("TIPO INPUT:", tipo)

                    if tipo == "text":

                        await campo.fill(
                            link_produto
                        )

                        print("LINK PREENCHIDO")

                        achou_input = True

                        break

                except:
                    pass

            if not achou_input:

                print("NAO ACHOU INPUT")

                html = await page.content()

                print(html[:5000])

                await browser.close()

                return link_produto

            await page.wait_for_timeout(3000)

            # PROCURA BOTÃO
            botoes = await page.locator(
                "button"
            ).all()

            clicou = False

            for botao in botoes:

                try:

                    texto_botao = await botao.inner_text()

                    print("BOTAO:", texto_botao)

                    if (
                        "Gerar" in texto_botao
                        or "Criar" in texto_botao
                        or "generar" in texto_botao.lower()
                    ):

                        await botao.click()

                        print("CLICOU GERAR")

                        clicou = True

                        break

                except:
                    pass

            if not clicou:

                print("NAO ACHOU BOTAO")

            await page.wait_for_timeout(8000)

            # PEGA HTML
            html = await page.content()

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

            print("NAO GEROU LINK")

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