from telethon import TelegramClient, events
import os
import re
import aiohttp
import traceback

from playwright.async_api import async_playwright

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


# ==========================================
# MERCADO LIVRE
# ==========================================

async def gerar_link_afiliado_ml(link_produto):

    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(
                link_produto,
                allow_redirects=True,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            ) as response:

                print("LINK ORIGINAL:", link_produto)

                # PEGA LINK FINAL REAL
                link_real = str(response.real_url)

                print("LINK REAL:", link_real)

                # REMOVE matt_tool
                link_real = re.sub(
                    r'&matt_tool=[^&]+',
                    '',
                    link_real
                )

                link_real = re.sub(
                    r'\?matt_tool=[^&]+&?',
                    '?',
                    link_real
                )

                # REMOVE matt_word
                link_real = re.sub(
                    r'&matt_word=[^&]+',
                    '',
                    link_real
                )

                link_real = re.sub(
                    r'\?matt_word=[^&]+&?',
                    '?',
                    link_real
                )

                # LIMPEZA
                link_real = link_real.replace("?&", "?")
                link_real = link_real.replace("&&", "&")

                if link_real.endswith("?"):
                    link_real = link_real[:-1]

                if link_real.endswith("&"):
                    link_real = link_real[:-1]

                # ADICIONA AFILIADO
                if "?" in link_real:

                    novo_link = (
                        link_real
                        + "&matt_tool=73653354"
                    )

                else:

                    novo_link = (
                        link_real
                        + "?matt_tool=73653354"
                    )

                print("NOVO LINK:", novo_link)

                return novo_link

    except Exception as e:

        print("ERRO AFILIADO ML:", e)

        traceback.print_exc()

        return link_produto


# ==========================================
# SHOPEE
# ==========================================

async def gerar_link_shopee(link_produto):

    try:

        print("===================================")
        print("INICIANDO PLAYWRIGHT SHOPEE 🔥")
        print("LINK:", link_produto)
        print("===================================")

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            await page.goto(
                "https://affiliate.shopee.com.br/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("SHOPEE ABERTA 🔥")

            titulo = await page.title()

            print("TITULO PAGINA:", titulo)

            await browser.close()

        return link_produto

    except Exception as e:

        print("ERRO PLAYWRIGHT SHOPEE:", e)

        traceback.print_exc()

        return link_produto


# ==========================================
# SHEIN
# ==========================================

async def gerar_link_shein(link_produto):

    try:

        print("===================================")
        print("INICIANDO PROCESSAMENTO SHEIN 🔥")
        print("LINK ORIGINAL:", link_produto)
        print("===================================")

        # POR ENQUANTO
        # RETORNA O MESMO LINK

        novo_link = link_produto

        print("LINK SHEIN FINAL:", novo_link)

        return novo_link

    except Exception as e:

        print("ERRO SHEIN:", e)

        traceback.print_exc()

        return link_produto


# ==========================================
# EVENTO TELEGRAM
# ==========================================

@client.on(events.NewMessage(
    chats=canais_monitorados,
    incoming=True
))
async def handler(event):

    try:

        print("===================================")
        print("MENSAGEM RECEBIDA 🔥")
        print("ID MSG:", event.id)
        print("===================================")

        # TEXTO
        texto = ""

        if event.message.message:

            texto = event.message.message

        elif event.message.raw_text:

            texto = event.message.raw_text

        elif event.text:

            texto = event.text

        texto = str(texto).strip()

        # SEM TEXTO E SEM FOTO
        if not texto and not event.photo:

            print("SEM TEXTO E SEM FOTO")
            return

        print("TEXTO ORIGINAL:")
        print(texto)

        # REMOVE MARCA D'ÁGUA
        texto = re.sub(
            r"📍.*",
            "",
            texto
        ).strip()

        print("TEXTO LIMPO:")
        print(texto)

        # PEGA LINKS
        links = re.findall(
            r"(https?://[^\s]+)",
            texto
        )

        print("LINKS ENCONTRADOS:", links)

        # SEM LINKS
        if not links:

            print("SEM LINKS NA MENSAGEM")

        # PROCESSA LINKS
        for i, link in enumerate(links):

            try:

                print("===================================")
                print(f"LINK {i+1}: {link}")
                print("ANALISANDO LINK...")
                print("===================================")

                # ==========================================
                # MERCADO LIVRE
                # ==========================================

                if (
                    "mercadolivre" in link.lower()
                    or "meli.la" in link.lower()
                ):

                    print("LINK ML DETECTADO 🔥")

                    novo_link = await gerar_link_afiliado_ml(link)

                    print("LINK NOVO:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # ==========================================
                # SHOPEE
                # ==========================================

                elif (

                    "shopee" in link.lower()
                    or "s.shopee.com.br" in link.lower()
                    or "shope.ee" in link.lower()
                    or "shp.ee" in link.lower()

                ):

                    print("LINK SHOPEE DETECTADO 🔥")

                    novo_link = await gerar_link_shopee(link)

                    print("LINK NOVO SHOPEE:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # ==========================================
                # SHEIN
                # ==========================================

                elif (

                    "shein" in link.lower()
                    or "onelink.shein.com" in link.lower()

                ):

                    print("LINK SHEIN DETECTADO 🔥")

                    novo_link = await gerar_link_shein(link)

                    print("LINK NOVO SHEIN:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                else:

                    print("LINK NÃO IDENTIFICADO")

                print("FIM PROCESSAMENTO LINK 🔥")

            except Exception as erro_link:

                print("ERRO NO LINK:", erro_link)

                traceback.print_exc()

        print("===================================")
        print("TEXTO FINAL:")
        print(texto)
        print("===================================")

        # ENVIA FOTO
        if event.photo:

            print("ENVIANDO FOTO 🔥")

            arquivo = await event.download_media()

            await client.send_file(
                canal_destino,
                arquivo,
                caption=texto,
                link_preview=False
            )

        # ENVIA TEXTO
        else:

            print("ENVIANDO TEXTO 🔥")

            await client.send_message(
                canal_destino,
                texto,
                link_preview=True
            )

        print("OFERTA ENVIADA 🔥")

    except Exception as e:

        print("ERRO GERAL:", e)

        traceback.print_exc()


client.run_until_disconnected()