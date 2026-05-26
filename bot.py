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

        # VERIFICA TEXTO
        if len(texto) < 2:
            return

        # NOME MANUAL
        titulo = texto[0]

        # LINK
        link = texto[1]

        # PREÇO
        preco = "💰 Confira a oferta"

        if len(texto) >= 3:
            preco = f"💰 R$ {texto[2]}"

        # CUPOM OPCIONAL
        cupom = ""

        if len(texto) >= 4:
            cupom = texto[3]

        # VALIDA LINK
        if "http" not in link:
            return

        # TESTA LINK
        try:

            requests.get(
                link,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=10
            )

        except:
            pass

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