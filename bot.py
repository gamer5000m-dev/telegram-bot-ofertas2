from telethon import TelegramClient, events
import os
import re
import traceback

# ==========================================
# CONFIGURAÇÃO
# ==========================================

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

canal_destino = -1003914285353

canais_monitorados = [
    -1001353489373
]

# ==========================================
# TELEGRAM
# ==========================================

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

client.start()

print("BOT ONLINE 🔥")

# ==========================================
# EVENTO TELEGRAM
# ==========================================

@client.on(events.NewMessage(
    chats=canais_monitorados,
    incoming=True
))
async def handler(event):

    try:

        print("===================================")
        print("MENSAGEM RECEBIDA 🔥")
        print("ID MSG:", event.id)
        print("===================================")

        texto = ""

        if event.message.message:

            texto = event.message.message

        elif event.message.raw_text:

            texto = event.message.raw_text

        elif event.text:

            texto = event.text

        texto = str(texto).strip()

        if not texto and not event.photo:

            return

        print("TEXTO ORIGINAL:")
        print(texto)

        # REMOVE MARCA
        texto = re.sub(
            r"📍.*",
            "",
            texto
        ).strip()

        # REMOVE TODOS OS LINKS
        texto = re.sub(
            r"https?://[^\s]+",
            "",
            texto
        ).strip()

        print("TEXTO FINAL:")
        print(texto)

        # ==========================================
        # ENVIO
        # ==========================================

        if event.photo:

            print("ENVIANDO FOTO 🔥")

            arquivo = await event.download_media()

            await client.send_file(
                canal_destino,
                arquivo,
                caption=texto,
                link_preview=False
            )

        else:

            print("ENVIANDO TEXTO 🔥")

            await client.send_message(
                canal_destino,
                texto,
                link_preview=False
            )

        print("OFERTA ENVIADA 🔥")

    except Exception as e:

        print("ERRO GERAL:", e)
        traceback.print_exc()

# ==========================================
# START
# ==========================================

client.run_until_disconnected()