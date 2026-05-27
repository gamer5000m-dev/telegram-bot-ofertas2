from telethon import TelegramClient, events
import os

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# SEU CANAL
canal_destino = "-1003914285353"

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

# LOGIN
client.start(
    phone="+5561994348181",
    code_callback=lambda: "82195"
)

print("BOT ONLINE 🔥")


# DEBUG PARA PEGAR ID DOS CANAIS
@client.on(events.NewMessage)
async def debug(event):

    try:

        print("CHAT ID:", event.chat_id)
        print("MENSAGEM:", event.raw_text)

        # TESTE
        await client.send_message(
            canal_destino,
            "TESTE FUNCIONANDO 🔥"
        )

    except Exception as e:

        print(e)


client.run_until_disconnected()