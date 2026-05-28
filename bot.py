from telethon import TelegramClient, events
import os
import re
import aiohttp
import traceback

# API TELEGRAM
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# CANAL DESTINO
canal_destino = -1003914285353

# CANAIS MONITORADOS
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
    phone="+5561994348181",
    code_callback=lambda: "82195"
)

print("BOT ONLINE 🔥")


# GERAR LINK AFILIADO ML
async def gerar_link_afiliado_ml(link_produto):

    try:

        async with aiohttp.ClientSession() as session:

            async with session.get(
                link_produto,
                allow_redirects=True,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            ) as response:

                print("LINK ORIGINAL:", link_produto)

                link_real = str(response.url)

                print("LINK REAL:", link_real)

                # REMOVE AFILIADOS ANTIGOS
                link_real = re.sub(
                    r'([&?])matt_tool=[^&]+',
                    '',
                    link_real
                )

                link_real = re.sub(
                    r'([&?])matt_word=[^&]+',
                    '',
                    link_real
                )

                # LIMPA ?& BUGADO
                link_real = link_real.replace("?&", "?")

                # REMOVE ? NO FINAL
                if link_real.endswith("?"):
                    link_real = link_real[:-1]

                # ADICIONA SEU AFILIADO
                if "?" in link_real:

                    novo_link = (
                        link_real
                        + "&matt_tool=73653354"
                    )

                else:

                    novo_link = (
                        link_real
                        + "?matt_tool=73653354"
                    )

                print("NOVO LINK:", novo_link)

                return novo_link

    except Exception as e:

        print("ERRO AFILIADO:", e)

        traceback.print_exc()

        return link_produto


@client.on(events.NewMessage(chats=canais_monitorados))
async def handler(event):

    try:

        print("MENSAGEM RECEBIDA")

        # PEGA TEXTO/CAPTION
        texto = event.message.message or ""

        if not texto:
            print("SEM TEXTO")
            return

        print("TEXTO:")
        print(texto)

        # REMOVE MARCA D'ÁGUA
        texto = re.sub(
            r"📍.*",
            "",
            texto
        ).strip()

        # PEGA LINKS
        links = re.findall(
            r"(https?://[^\s]+)",
            texto
        )

        print("LINKS ENCONTRADOS:", links)

        # PROCESSA LINKS
        for link in links:

            print("PROCESSANDO:", link)

            # MERCADO LIVRE
            if (
                "mercadolivre" in link.lower()
                or "meli.la" in link.lower()
            ):

                novo_link = await gerar_link_afiliado_ml(link)

                print("LINK NOVO:", novo_link)

                texto = re.sub(
                    re.escape(link),
                    novo_link,
                    texto
                )

        print("TEXTO FINAL:")
        print(texto)

        # ENVIA FOTO + TEXTO
        if event.photo:

            arquivo = await event.download_media()

            await client.send_file(
                canal_destino,
                arquivo,
                caption=texto,
                link_preview=False
            )

        else:

            await client.send_message(
                canal_destino,
                texto,
                link_preview=True
            )

        print("Oferta enviada 🔥")

    except Exception as e:

        print("ERRO GERAL:", e)

        traceback.print_exc()


client.run_until_disconnected()