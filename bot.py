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

        # MENSAGEM
        mensagem = f"""
🔥 OFERTA IMPERDÍVEL

{preco}
"""

        # MOSTRA CUPOM SOMENTE SE EXISTIR
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