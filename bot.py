import requests
import cloudscraper
from bs4 import BeautifulSoup

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

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
    timeout=10
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
        elif "mercadolivre" in url:
            produto = soup.find("h1")

            if produto:
                titulo = produto.get_text().strip()

        # SHOPEE
        elif "shopee" in url:
            if soup.title:
                titulo = soup.title.text.strip()
                titulo = titulo.replace("| Shopee Brasil", "")

        # SHEIN
        elif "shein" in url:
            if soup.title:
                titulo = soup.title.text.strip()
                titulo = titulo.replace("| SHEIN Brasil", "")

        # OUTROS
        else:
            if soup.title:
                titulo = soup.title.text.strip()

        if titulo == "":
            titulo = "Oferta imperdível"

        return titulo[:80]

    except:
        return "Oferta imperdível"


async def responder(update, context):
    try:
        link = update.message.text

        if "http" not in link:
            return

        link = requests.get(
            link,
            headers={"User-Agent": "Mozilla/5.0"}
        ).url.split("?")[0]

        titulo = pegar_titulo(link)

        if "shopee" in link:
            loja = "🛍 OFERTA SHOPEE"

        elif "amazon" in link:
            loja = "📦 OFERTA AMAZON"

        elif "mercadolivre" in link or "meli" in link:
            loja = "🛒 OFERTA MERCADO LIVRE"

        elif "shein" in link:
            loja = "👗 OFERTA SHEIN"

        else:
            loja = "🔥 SUPER OFERTA"

        mensagem = f"""
━━━━━━━━━━━━━━━

{loja}

🛍 {titulo}

👇 Clique no botão abaixo

━━━━━━━━━━━━━━━

#promoção #ofertas #desconto

<a href="{link}">⠀</a>
"""

        teclado = [
            [
                InlineKeyboardButton(
                    "🛒 COMPRAR AGORA",
                    url=link
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(teclado)

        await context.bot.send_message(
            chat_id=CANAL,
            text=mensagem,
            parse_mode="HTML",
            disable_web_page_preview=False,
            reply_markup=reply_markup
        )

    except Exception as e:
        print(e)


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE!")

app.run_polling()