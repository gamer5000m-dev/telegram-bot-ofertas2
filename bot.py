import requests
import cloudscraper
from bs4 import BeautifulSoup

from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

import os

TOKEN = os.getenv("TOKEN")

CANAL = "-1003914285353"


def pegar_titulo(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            ),
            "Accept-Language": "pt-BR,pt;q=0.9"
        }

        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "mobile": False
            }
        )

        resposta = scraper.get(
            url,
            headers=headers,
            timeout=20
        )

        html = resposta.text

        titulo = ""

        # AMAZON
        if "amazon" in url:

            if 'id="productTitle"' in html:

                inicio = html.find(
                    'id="productTitle"'
                )

                html2 = html[inicio:]

                inicio2 = html2.find(">") + 1
                fim2 = html2.find("<", inicio2)

                titulo = html2[inicio2:fim2].strip()

        # OUTRAS LOJAS
        if titulo == "":

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            # og:title
            meta = soup.find(
                "meta",
                property="og:title"
            )

            if meta:
                titulo = meta.get("content")

            # h1 fallback
            if titulo == "":

                h1 = soup.find("h1")

                if h1:
                    titulo = h1.get_text().strip()

            # title fallback
            if titulo == "" and soup.title:

                titulo = soup.title.text.strip()

        # LIMPEZA
        remover = [
            "| Amazon.com.br",
            "| Shopee Brasil",
            "| SHEIN Brasil",
            "| Mercado Livre",
            "Mercado Livre Brasil - Onde comprar e vender de Tudo"
        ]

        for texto in remover:

            titulo = titulo.replace(
                texto,
                ""
            )

        titulo = titulo.strip()

        # FALLBACK FINAL
        if titulo == "":
            titulo = "Oferta imperdível"

        return titulo

    except Exception as e:

        print(e)

        return "Oferta imperdível"


async def responder(update, context):

    try:

        # FOTO + LEGENDA
        if update.message.photo:

            texto = update.message.caption.splitlines()

            foto = update.message.photo[-1].file_id

        # SOMENTE TEXTO
        else:

            texto = update.message.text.splitlines()

            foto = None

        if len(texto) == 0:
            return

        link = texto[0]

        # PREÇO
        preco = "💰 Confira a oferta"

        if len(texto) >= 2:
            preco = f"💰 R$ {texto[1]}"

        # CUPOM OPCIONAL
        cupom = ""

        if len(texto) >= 3:
            cupom = texto[2]

        # VALIDA LINK
        if "http" not in link:
            return

        # PEGA LINK FINAL
        try:

            link_final = requests.get(
                link,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                allow_redirects=True,
                timeout=20
            ).url

        except:

            link_final = link

        # PEGA NOME REAL
        titulo = pegar_titulo(link_final)

        # MONTA MENSAGEM
        mensagem = f"""
🛍 {titulo}

{preco}
"""

        # CUPOM OPCIONAL
        if cupom != "":

            mensagem += f"""

🎟 CUPOM: {cupom}
"""

        mensagem += f"""

🔗 {link_final}
"""

        # ENVIA COM FOTO
        if foto:

            await context.bot.send_photo(
                chat_id=CANAL,
                photo=foto,
                caption=mensagem
            )

        # ENVIA SEM FOTO
        else:

            await context.bot.send_message(
                chat_id=CANAL,
                text=mensagem,
                disable_web_page_preview=False
            )

    except Exception as e:

        print(e)


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL, responder)
)

print("BOT ONLINE!")

app.run_polling()