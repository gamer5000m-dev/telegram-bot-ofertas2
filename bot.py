import requests
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

CANAL = ""


def pegar_titulo(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resposta = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        if soup.title:
            titulo = soup.title.text.strip()

            titulo = titulo.replace("| Amazon.com.br", "")
            titulo = titulo.replace("- Mercado Livre", "")
            titulo = titulo.replace("| Shopee Brasil", "")
            titulo = titulo.replace("| SHEIN Brasil", "")

            return titulo[:80]

        return "Oferta imperdível"

    except:
        return "Oferta imperdível"


async def responder(update, context):
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

    try:
        await context.bot.send_photo(
            chat_id=CANAL,
            photo=link,
            caption=mensagem,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    except:
        await context.bot.send_message(
            chat_id=CANAL,
            text=mensagem,
            parse_mode="HTML",
            disable_web_page_preview=False,
            reply_markup=reply_markup
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE!")

app.run_polling()