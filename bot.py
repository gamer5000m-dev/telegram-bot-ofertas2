import requests

from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

import os

TOKEN = os.getenv("TOKEN")

CANAL = "-1003914285353"


async def responder(update, context):

    try:

        # FOTO + LEGENDA
        if update.message.photo:

            texto = update.message.caption.splitlines()

        # SOMENTE TEXTO
        else:

            texto = update.message.text.splitlines()

        link = texto[0]

        preco = "💰 Confira a oferta"

        cupom = "OFERTA10"

        # PREÇO
        if len(texto) >= 2:
            preco = f"💰 R$ {texto[1]}"

        # CUPOM
        if len(texto) >= 3:
            cupom = texto[2]

        if "http" not in link:
            return

        # LIMPA LINKS GIGANTES
        link = requests.get(
            link,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        ).url.split("?")[0]

        mensagem = f"""
🔥 OFERTA IMPERDÍVEL

{preco}

🎟 CUPOM: {cupom}

🔗 {link}
"""

        # ENVIA MENSAGEM COM PREVIEW AUTOMÁTICO
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