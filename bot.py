import requests

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


async def responder(update, context):
    link = update.message.text

    if "http" not in link:
        return

    link = requests.get(
    link,
    headers={"User-Agent": "Mozilla/5.0"}
).url.split("?")[0]

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

🔥 Promoção disponível agora

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

    await context.bot.send_photo(
    chat_id=CANAL,
    photo=link,
    caption=mensagem,
    parse_mode="HTML",
    reply_markup=reply_markup
)


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE!")

app.run_polling()