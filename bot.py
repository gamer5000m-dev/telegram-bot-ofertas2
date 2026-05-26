from telethon import TelegramClient, events
import re
import os

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# SEU CANAL
canal_destino = "-1003914285353"

# CANAL MONITORADO
canais_monitorados = [
    "canaldeofertasecupons"
]

client = TelegramClient(
    "session",
    api_id,
    api_hash
)

@client.on(events.NewMessage(chats=canais_monitorados))
async def handler(event):

    texto = event.raw_text

    links = re.findall(
        r'https?://\S+',
        texto
    )

    # IGNORA SEM LINK
    if not links:
        return

    # ENVIA NO SEU CANAL
    await client.send_message(
        canal_destino,
        texto,
        link_preview=True
    )

    print("Oferta enviada")


print("MONITORANDO...")

client.start(phone="+5561994348181")

client.run_until_disconnected()