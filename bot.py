from telethon import TelegramClient, events
import re
import os

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# SEU CANAL
canal_destino = "-1003914285353"

# CANAL MONITORADO
canais_monitorados = None

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

@client.on(events.NewMessage)
async def handler(event):

    texto = event.raw_text

    print("MENSAGEM:", texto)

    await client.send_message(
        canal_destino,
        "TESTE"
    )


print("MONITORANDO...")

client.start(
    phone="+5561994348181",
    code_callback=lambda: "82195"
)

client.run_until_disconnected()