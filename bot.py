from telethon import TelegramClient, events
import os
import re
import traceback

# ==========================================
# CONFIG
# ==========================================

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

canal_destino = -1003914285353

canais_monitorados = [
    -1001353489373
]

# ==========================================
# TELEGRAM
# ==========================================

client = TelegramClient(
    "/data/session",
    api_id,
    api_hash
)

ofertas_pendentes = {}

# ==========================================
# RECEBE OFERTAS
# ==========================================

@client.on(events.NewMessage(
    chats=canais_monitorados
))
async def receber_oferta(event):

    try:

        texto = event.raw_text or ""

        # TROCA FRASE
        texto = re.sub(
            r".*Preço e estoque limitados.*",
            "🔥 Oferta relâmpago! Aproveite já!",
            texto
        )

        # TROCA LINK POR MARCADOR
        texto = re.sub(
            r"https?://[^\s]+",
            "{LINK}",
            texto
        )

        if not texto and not event.photo:
            return

        foto = None

        if event.photo:
            foto = await event.download_media()

        mensagem = (
            "🔥 NOVA OFERTA\n\n"
            f"{texto}\n\n"
            "➡️ RESPONDA ESTA MENSAGEM COM SEU LINK."
        )

        if foto:

            enviada = await client.send_file(
                "me",
                foto,
                caption=mensagem
            )

        else:

            enviada = await client.send_message(
                "me",
                mensagem
            )

        ofertas_pendentes[enviada.id] = {
            "texto": texto,
            "foto": foto
        }

        print("OFERTA ENVIADA PARA ME")
        print("ID:", enviada.id)

    except Exception as e:

        print("ERRO RECEBER OFERTA:", e)
        traceback.print_exc()

# ==========================================
# RECEBE LINK
# ==========================================

@client.on(events.NewMessage(chats="me"))
async def responder_link(event):

    try:

        if not event.is_reply:
            return

        resposta = await event.get_reply_message()

        if resposta.id not in ofertas_pendentes:
            return

        link = event.raw_text.strip()

        dados = ofertas_pendentes[resposta.id]

        texto_final = dados["texto"].replace(
            "{LINK}",
            link
        )

        if dados["foto"]:

            await client.send_file(
                canal_destino,
                dados["foto"],
                caption=texto_final,
                link_preview=False
            )

        else:

            await client.send_message(
                canal_destino,
                texto_final,
                link_preview=False
            )

        await event.reply(
            "✅ Oferta publicada."
        )

        del ofertas_pendentes[resposta.id]

        print("OFERTA PUBLICADA")

    except Exception as e:

        print("ERRO PUBLICAR:", e)
        traceback.print_exc()

# ==========================================
# START
# ==========================================

print("BOT ONLINE 🔥")

client.start()
client.run_until_disconnected()