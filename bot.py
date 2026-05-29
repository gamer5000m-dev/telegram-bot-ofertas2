from telethon import TelegramClient, events
import os
import re
import traceback

# ==========================================
# VARIAVEIS
# ==========================================

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# ==========================================
# TELEGRAM
# ==========================================

canal_destino = -1003914285353

canais_monitorados = [
    -1001353489373
]

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

client.start()

print("BOT ONLINE 🔥")

# ==========================================
# MERCADO LIVRE
# ==========================================

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

                link_real = str(response.real_url)

                print("LINK REAL:", link_real)

                # REMOVE AFILIADOS ANTIGOS
                link_real = re.sub(
                    r'&matt_tool=[^&]+',
                    '',
                    link_real
                )

                link_real = re.sub(
                    r'\?matt_tool=[^&]+&?',
                    '?',
                    link_real
                )

                link_real = re.sub(
                    r'&matt_word=[^&]+',
                    '',
                    link_real
                )

                link_real = re.sub(
                    r'\?matt_word=[^&]+&?',
                    '?',
                    link_real
                )

                # LIMPEZA
                link_real = link_real.replace("?&", "?")
                link_real = link_real.replace("&&", "&")

                if link_real.endswith("?"):
                    link_real = link_real[:-1]

                if link_real.endswith("&"):
                    link_real = link_real[:-1]

                # SEU AFILIADO
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

        print("ERRO AFILIADO ML:", e)

        traceback.print_exc()

        return link_produto

# ==========================================
# SHOPEE
# ==========================================

 ==========================================
           

# ==========================================
# SHEIN
# ==========================================


      

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

        print("TEXTO LIMPO:")
        print(texto)

        # LINKS
        links = re.findall(
            r"(https?://[^\s]+)",
            texto
        )

        print("LINKS ENCONTRADOS:", links)

        # ==========================================
        # PROCESSA LINKS
        # ==========================================

        for i, link in enumerate(links):

            try:

                print("===================================")
                print(f"LINK {i+1}: {link}")
                print("ANALISANDO LINK...")
                print("===================================")

                # ==========================================
                # MERCADO LIVRE
                # ==========================================
 
==========================================
                # SHOPEE
                # =================================== ==========================================
                # SHEIN
                # ==========================================

    ==========================================
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
                link_preview=True
            )

        print("OFERTA ENVIADA 🔥")

    except Exception as e:

        print("ERRO GERAL:", e)

        traceback.print_exc()

# ==========================================
# START
# ==========================================

client.run_until_disconnected()