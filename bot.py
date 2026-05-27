from telethon import TelegramClient, events
import os

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# ID DO SEU CANAL
canal_destino = -1003914285353

# ID DO CANAL MONITORADO
canais_monitorados = [
    -1001353489373
]

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

# LOGIN
client.start(
    phone="+5561994348181"
)

print("BOT ONLINE 🔥")


@client.on(events.NewMessage(chats=canais_monitorados))
async def handler(event):

    try:

        texto = event.raw_text

        if not texto:
            return

        # SE TIVER FOTO
        if event.photo:

            caminho = await event.download_media()

            await client.send_file(
                canal_destino,
                caminho,
                caption=texto,
                link_preview=False
            )

        else:

            # SÓ TEXTO
            await client.send_message(
                canal_destino,
                texto,
                link_preview=False
            )

        print("Oferta enviada 🔥")

    except Exception as e:

        print(e)


client.run_until_disconnected()