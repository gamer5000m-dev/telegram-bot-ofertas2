from telethon import TelegramClient, events
import os
import re
import requests

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

        # MERCADO LIVRE AFILIADO
links = re.findall(
    r'https?://[^\s]+',
    texto
)

for link in links:

    if (
        "mercadolivre" in link.lower()
        or "meli.la" in link.lower()
    ):

        try:

            print("LINK ORIGINAL:", link)

            # EXPANDE LINK
            response = requests.get(
                link,
                allow_redirects=True,
                timeout=10
            )

            link_real = response.url

            print("LINK REAL:", link_real)

            # REMOVE PARAMETROS ANTIGOS
            link_real = link_real.split("&matt_tool=")[0]

            # ADICIONA SEU AFILIADO
            if "?" in link_real:

                novo_link = (
                    link_real +
                    "&matt_tool=73653354"
                )

            else:

                novo_link = (
                    link_real +
                    "?matt_tool=73653354"
                )

            print("NOVO LINK:", novo_link)

            texto = texto.replace(
                link,
                novo_link
            )

        except Exception as e:

            print("ERRO ML:", e)

    except Exception as e:

        print(e)


client.run_until_disconnected()