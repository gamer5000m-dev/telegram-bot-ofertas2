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

            if not update.message.caption:
                print("Sem legenda")
                return

            texto = update.message.caption.splitlines()

            foto = update.message.photo[-1].file_id

        # SOMENTE TEXTO
        else:

            if not update.message.text:
                print("Sem texto")
                return

            texto = update.message.text.splitlines()

            foto = None

        print(texto)

        # FORMATO MÍNIMO
        if len(texto) < 2:

            print("Formato inválido")

            return

        # NOME DO PRODUTO
        titulo = texto[0].strip()

        # LINK
        link = texto[1].strip()

        # VALIDA LINK
        if "http" not in link:

            print("Link inválido")

            return

        # PREÇO
        preco = "💰 Confira a oferta"

        if len(texto) >= 3:

            if texto[2].strip() != "":
                preco = f"💰 R$ {texto[2].strip()}"

        # CUPOM OPCIONAL
        cupom = ""

        if len(texto) >= 4:
            cupom = texto[3].strip()

        # TESTA LINK
        try:

            requests.get(
                link,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=10
            )

        except Exception as erro:

            print(erro)

        # MENSAGEM
        mensagem = f"""
🛍 {titulo}

{preco}
"""

        # CUPOM
        if cupom != "":

            mensagem += f"""

🎟 CUPOM: {cupom}
"""

        # LINK
        mensagem += f"""

🔗 {link}
"""

        # ENVIA FOTO
        if foto:

            await context.bot.send_photo(
                chat_id=CANAL,
                photo=foto,
                caption=mensagem
            )

        # ENVIA TEXTO
        else:

            await context.bot.send_message(
                chat_id=CANAL,
                text=mensagem,
                disable_web_page_preview=False
            )

        print("Mensagem enviada")

    except Exception as e:

        print("ERRO:", e)


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL, responder)
)

print("BOT ONLINE!")

app.run_polling()