from telethon import TelegramClient, events
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

canal_destino = "-1003914285353"

@client.on(events.NewMessage)
async def handler(event):

    print("MENSAGEM RECEBIDA")

    await client.send_message(
        canal_destino,
        "TESTE FUNCIONANDO 🔥"
    )

print("BOT ONLINE")

client.start(
    phone="+5561994348181"
)

client.run_until_disconnected()