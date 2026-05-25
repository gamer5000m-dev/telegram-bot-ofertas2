import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

TOKEN = "8391542912:AAH1cduJ0E7naPhA0z6uezCgkbLn1BjyQDE"

CANAL = "-1003914285353"


async def responder(update, context):
    link = update.message.text

    if "http" not in link:
        return

    link = requests.get(link).url.split("?")[0]

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

{link}
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
        disable_web_page_preview=False,
        reply_markup=reply_markup
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE!")

app.run_polling()