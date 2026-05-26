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
            "User-Agent": "Mozilla/5.0"
        }

        scraper = cloudscraper.create_scraper()

        resposta = scraper.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        titulo = ""

        # AMAZON
        if "amazon" in url:

            produto = soup.find(id="productTitle")

            if produto:
                titulo = produto.get_text().strip()

        # MERCADO LIVRE
        elif "mercadolivre" in url or "meli" in url:

            produto = soup.find("h1")

            if produto:
                titulo = produto.get_text().strip()

        # SHOPEE
        elif "shopee" in url:

            meta = soup.find(
                "meta",
                property="og:title"
            )

            if meta:
                titulo = meta.get("content")

        # SHEIN
        elif "shein" in url:

            meta = soup.find(
                "meta",
                property="og:title"
            )

            if meta:
                titulo = meta.get("content")

        # OUTROS
        else:

            if soup.title:
                titulo = soup.title.text.strip()

        titulo = titulo.replace(
            "| Amazon.com.br",
            ""
        )

        titulo = titulo.replace(
            "| Shopee Brasil",
            ""
        )

        titulo = titulo.replace(
            "| SHEIN Brasil",
            ""
        )

        titulo = titulo.strip()

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

        link = texto[0]

        preco = "💰 Confira a oferta"

        # PREÇO
        if len(texto) >= 2:
            preco = f"💰 R$ {texto[1]}"

        # CUPOM OPCIONAL
        cupom = ""

        if len(texto) >= 3:
            cupom = texto[2]

        if "http" not in link:
            return

        # LIMPA LINK
        link = requests.get(
            link,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        ).url.split("?")[0]

        # PEGA NOME REAL DO PRODUTO
        titulo = pegar_titulo(link)

        # MONTA MENSAGEM
        mensagem = f"""
🛍 {titulo}

{preco}
"""

        # CUPOM OPCIONAL
        if cupom != "":
            mensagem += f"\n🎟 CUPOM: {cupom}\n"

        mensagem += f"""

🔗 {link}
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