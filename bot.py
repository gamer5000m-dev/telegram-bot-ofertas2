from telethon import TelegramClient, events
import os
import re

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

        # REMOVE PROPAGANDA
        remover = [
            "eieutil.com/ofertasecupons",
            "@canaldeofertasecupons"
        ]

        for r in remover:
            texto = texto.replace(r, "")

        texto = texto.strip()

        # PEGA LINKS
        links = re.findall(
            r'https?://\S+',
            texto
        )

        # ADICIONA AFILIADO ML
        for link in links:

            if "mercadolivre" in link.lower() or "meli.la" in link.lower():

                # JÁ TEM AFILIADO
                if "matt_tool=" in link:
                    continue

                # ADICIONA SEU AFILIADO
                if "?" in link:

                    novo_link = (
                        link +
                        "&matt_tool=73653354"
                    )

                else:

                    novo_link = (
                        link +
                        "?matt_tool=73653354"
                    )

                texto = texto.replace(
                    link,
                    novo_link
                )

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

            await client.send_message(
                canal_destino,
                texto,
                link_preview=False
            )

        print("Oferta enviada 🔥")

    except Exception as e:

        print(e)


client.run_until_disconnected()