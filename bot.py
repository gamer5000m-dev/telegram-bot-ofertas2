from telethon import TelegramClient, events
import os
import re
import requests

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# ID DO SEU CANAL
canal_destino = -1003914285353

# ID DOS CANAIS MONITORADOS
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

        # DEBUG
        print(event.message)

        # TEXTO
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
            r'https?://[^\s]+',
            texto
        )

        # MERCADO LIVRE AFILIADO
        for link in links:

            if (
                "mercadolivre" in link.lower()
                or "meli.la" in link.lower()
            ):

                try:

                    print("LINK ORIGINAL:", link)

                    # FORÇA EXPANSÃO
                    response = requests.get(
                        link,
                        allow_redirects=True,
                        timeout=10,
                        headers={
                            "User-Agent": (
                                "Mozilla/5.0"
                            )
                        }
                    )

                    link_real = str(response.url)

                    # TENTA PEGAR REDIRECT REAL
                    if "meli.la" in link_real:

                        try:

                            link_real = response.history[-1].headers.get(
                                "location",
                                link_real
                            )

                        except:

                            pass

                    print("LINK REAL:", link_real)

                    # REMOVE AFILIADO ANTIGO
                    if "&matt_tool=" in link_real:
                        link_real = link_real.split("&matt_tool=")[0]

                    if "?matt_tool=" in link_real:
                        link_real = link_real.split("?matt_tool=")[0]

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

                    # TROCA LINK
                    texto = texto.replace(
                        link,
                        novo_link
                    )

                except Exception as e:

                    print("ERRO ML:", e)

        # SE TIVER FOTO
        if event.photo:

            # BAIXA FOTO LIMPA
            await event.download_media(
                file="temp.jpg"
            )

            # ENVIA FOTO NOVA
            await client.send_file(
                canal_destino,
                file="temp.jpg",
                caption=str(texto),
                parse_mode=None,
                formatting_entities=[],
                link_preview=False
            )

        else:

            # ENVIA TEXTO LIMPO
            await client.send_message(
                canal_destino,
                str(texto),
                parse_mode=None,
                formatting_entities=[],
                link_preview=False
            )

        print("Oferta enviada 🔥")

    except Exception as e:

        print(e)


client.run_until_disconnected()