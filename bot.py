import random
import requests
import cloudscraper
from bs4 import BeautifulSoup

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    MessageHandler,
    filters,
)

import os

TOKEN = os.getenv("TOKEN")

CANAL = "-1003914285353"


def pegar_titulo(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        scraper = cloudscraper.create_scraper()

        resposta = scraper.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        titulo = ""

        # AMAZON
        if "amazon" in url:
            produto = soup.find(id="productTitle")

            if produto:
                titulo = produto.get_text().strip()

        # MERCADO LIVRE
        elif "mercadolivre" in url:
            produto = soup.find("h1")

            if produto:
                titulo = produto.get_text().strip()

        # SHOPEE
        elif "shopee" in url:
            if soup.title:
                titulo = soup.title.text.strip()
                titulo = titulo.replace("| Shopee Brasil", "")

        # SHEIN
        elif "shein" in url:
            if soup.title:
                titulo = soup.title.text.strip()
                titulo = titulo.replace("| SHEIN Brasil", "")

        # OUTROS
        else:
            if soup.title:
                titulo = soup.title.text.strip()

        if titulo == "":

            if "amazon" in url:
                titulo = "Promoção Amazon"

            elif "mercadolivre" in url:
                titulo = "Oferta Mercado Livre"

            elif "shopee" in url:
                titulo = "Oferta Shopee"

            elif "shein" in url:
                titulo = "Oferta SHEIN"

            else:
                titulo = "Oferta imperdível"

        if len(titulo) > 55:
            return titulo[:55] + "..."

        return titulo

    except:
        return "Oferta imperdível"


def pegar_preco(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        scraper = cloudscraper.create_scraper()

        resposta = scraper.get(
            url,
            headers=headers,
            timeout=10
        )

        html = resposta.text

        preco = ""

        # AMAZON
        if "amazon" in url:

            if 'a-price-whole' in html:

                inicio = html.find('a-price-whole">') + 16
                fim = html.find('<', inicio)

                valor = html[inicio:fim]

                preco = valor

                if 'a-price-fraction' in html:

                    inicio2 = html.find('a-price-fraction">') + 19
                    fim2 = html.find('<', inicio2)

                    centavos = html[inicio2:fim2]

                    preco += "," + centavos

        # MERCADO LIVRE
        elif "mercadolivre" in url:

            if 'andes-money-amount__fraction' in html:

                inicio = html.find(
                    'andes-money-amount__fraction'
                )

                html2 = html[inicio:]

                inicio2 = html2.find(">") + 1
                fim2 = html2.find("<", inicio2)

                preco = html2[inicio2:fim2]

        if preco != "":
            return f"💰 R$ {preco}"

        return "💥 Oferta especial"

    except:
        return "💥 Oferta especial"


def pegar_imagem(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        scraper = cloudscraper.create_scraper()

        resposta = scraper.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        imagem = None

        # AMAZON
        if "amazon" in url:

            img = soup.find(id="landingImage")

            if img:
                imagem = img.get("src")

        # MERCADO LIVRE
        elif "mercadolivre" in url:

            img = soup.find("img")

            if img:
                imagem = img.get("src")

        # SHOPEE
        elif "shopee" in url:

            img = soup.find("img")

            if img:
                imagem = img.get("src")

        # SHEIN
        elif "shein" in url:

            img = soup.find("img")

            if img:
                imagem = img.get("src")

        return imagem

    except:
        return None


async def responder(update, context):
    try:
        link = update.message.text

        if "http" not in link:
            return

        link = requests.get(
            link,
            headers={"User-Agent": "Mozilla/5.0"}
        ).url.split("?")[0]

        titulo = pegar_titulo(link)

        preco = pegar_preco(link)

        imagem = pegar_imagem(link)

        if "shopee" in link:
            loja = "🛍 OFERTA SHOPEE"

        elif "amazon" in link:
            loja = "📦 OFERTA AMAZON"

        elif "mercadolivre" in link or "meli" in link:
            loja = "🛒 OFERTA MERCADO LIVRE"

        elif "shein" in link:
            loja = "👗 OFERTA SHEIN"

        else:
            loja = "🔥 SUPER OFERTA"

        frases = [
            "🔥 Oferta relâmpago",
            "⚠️ Últimas unidades",
            "💥 Preço promocional",
            "🚀 Aproveite agora",
            "🤑 Desconto disponível",
            "🎯 Oferta do dia"
        ]

        frase = random.choice(frases)

        mensagem = f"""
━━━━━━━━━━━━━━━

{loja}

🛍 {titulo}

{preco}

{frase}

👇 Clique no botão abaixo

━━━━━━━━━━━━━━━

#promoção #ofertas #desconto

<a href="{link}">⠀</a>
"""

        teclado = [
            [
                InlineKeyboardButton(
                    "🛒 COMPRAR AGORA",
                    url=link
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(teclado)

        if imagem:

            await context.bot.send_photo(
                chat_id=CANAL,
                photo=imagem,
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

        else:

            await context.bot.send_message(
                chat_id=CANAL,
                text=mensagem,
                parse_mode="HTML",
                disable_web_page_preview=False,
                reply_markup=reply_markup
            )

    except Exception as e:
        print(e)


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT ONLINE!")

app.run_polling()