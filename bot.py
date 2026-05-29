import re
import os
import aiohttp
import asyncio

from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

CANAL_ORIGEM = int(os.getenv("CANAL_ORIGEM"))
CANAL_DESTINO = int(os.getenv("CANAL_DESTINO"))

client = TelegramClient(
    "bot_session",
    API_ID,
    API_HASH
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


# =========================================
# PEGAR HTML
# =========================================

async def pegar_html(url):

    async with aiohttp.ClientSession(
        headers=HEADERS
    ) as session:

        async with session.get(
            url,
            allow_redirects=True
        ) as response:

            return await response.text()


# =========================================
# PEGAR TITULO
# =========================================

def pegar_titulo(html):

    padroes = [

        r'<meta property="og:title" content="(.*?)"',
        r'<title>(.*?)</title>',

    ]

    for padrao in padroes:

        resultado = re.search(
            padrao,
            html,
            re.IGNORECASE
        )

        if resultado:

            titulo = resultado.group(1)

            titulo = re.sub(
                r'\s+',
                ' ',
                titulo
            ).strip()

            return titulo

    return "Oferta Imperdível"


# =========================================
# PEGAR PRECO
# =========================================

def pegar_preco(html):

    padroes = [

        r'R\$ ?[\d\.\,]+',
        r'price.?content.?="([\d\.\,]+)"',

    ]

    for padrao in padroes:

        resultado = re.search(
            padrao,
            html,
            re.IGNORECASE
        )

        if resultado:

            preco = resultado.group(0)

            if "R$" not in preco:
                preco = f"R$ {preco}"

            return preco

    return None


# =========================================
# PEGAR IMAGEM
# =========================================

def pegar_imagem(html):

    padroes = [

        r'<meta property="og:image" content="(.*?)"',
        r'<meta name="twitter:image" content="(.*?)"',

    ]

    for padrao in padroes:

        resultado = re.search(
            padrao,
            html,
            re.IGNORECASE
        )

        if resultado:

            return resultado.group(1)

    return None


# =========================================
# DETECTAR PLATAFORMA
# =========================================

def detectar_plataforma(url):

    url = url.lower()

    if "shopee" in url:
        return "Shopee", "🟠"

    if "mercadolivre" in url:
        return "Mercado Livre", "🟡"

    if "shein" in url:
        return "Shein", "⚫️"

    return "Oferta", "🔥"


# =========================================
# MONTAR TEXTO
# =========================================

def montar_texto(
    titulo,
    preco,
    plataforma,
    emoji,
    link
):

    texto = (
        f"{emoji} {titulo} | #{plataforma}:\n\n"
    )

    if preco:

        texto += (
            f"✅ {preco}\n\n"
        )

    texto += (
        f"🛒 COMPRE AQUI:\n"
        f"🔗 {link}\n\n"
        f"✳️ Preço e estoque limitados!"
    )

    return texto


# =========================================
# BAIXAR FOTO
# =========================================

async def baixar_foto(url):

    try:

        async with aiohttp.ClientSession(
            headers=HEADERS
        ) as session:

            async with session.get(url) as response:

                if response.status != 200:
                    return None

                conteudo = await response.read()

                with open(
                    "produto.jpg",
                    "wb"
                ) as f:

                    f.write(conteudo)

                return "produto.jpg"

    except:
        return None


# =========================================
# PEGAR LINKS
# =========================================

def pegar_links(texto):

    return re.findall(
        r'https?://[^\s]+',
        texto
    )


# =========================================
# PROCESSAR OFERTA
# =========================================

async def processar_oferta(link):

    print("")
    print("PROCESSANDO 🔥")
    print(link)

    plataforma, emoji = detectar_plataforma(link)

    html = await pegar_html(link)

    titulo = pegar_titulo(html)

    preco = pegar_preco(html)

    imagem = pegar_imagem(html)

    texto = montar_texto(
        titulo,
        preco,
        plataforma,
        emoji,
        link
    )

    print("")
    print("TEXTO FINAL 🔥")
    print(texto)

    foto = None

    if imagem:

        print("")
        print("BAIXANDO FOTO 🔥")

        foto = await baixar_foto(imagem)

    try:

        if foto and os.path.exists(foto):

            await client.send_file(
                CANAL_DESTINO,
                foto,
                caption=texto
            )

            os.remove(foto)

        else:

            await client.send_message(
                CANAL_DESTINO,
                texto
            )

        print("")
        print("OFERTA ENVIADA 🔥")

    except Exception as erro:

        print("")
        print("ERRO AO ENVIAR 🔥")
        print(erro)


# =========================================
# NOVA MENSAGEM
# =========================================

@client.on(
    events.NewMessage(
        chats=CANAL_ORIGEM
    )
)

async def handler(event):

    try:

        texto = event.raw_text

        print("")
        print("===================================")
        print("MENSAGEM RECEBIDA 🔥")
        print("===================================")

        links = pegar_links(texto)

        if not links:

            print("SEM LINKS")
            return

        print("")
        print("LINKS ENCONTRADOS 🔥")
        print(links)

        for link in links:

            try:

                await processar_oferta(link)

                await asyncio.sleep(2)

            except Exception as erro:

                print("")
                print("ERRO PROCESSANDO LINK 🔥")
                print(erro)

    except Exception as erro:

        print("")
        print("ERRO GERAL 🔥")
        print(erro)


# =========================================
# INICIAR
# =========================================

print("")
print("BOT ONLINE 🔥")
print("")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception(
        "BOT_TOKEN não encontrado nas variáveis do Railway"
    )

client.start(
    bot_token=BOT_TOKEN
)

client.run_until_disconnected()