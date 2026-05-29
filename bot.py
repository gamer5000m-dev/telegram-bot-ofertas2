from telethon import TelegramClient, events
import os
import re
import aiohttp
import traceback

from playwright.async_api import async_playwright

# ==========================================
# VARIAVEIS
# ==========================================

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

SHOPEE_LOGIN = os.getenv("SHOPEE_LOGIN")
SHOPEE_SENHA = os.getenv("SHOPEE_SENHA")

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

async def gerar_link_shopee(link_produto):

    browser = None

    try:

        print("===================================")
        print("INICIANDO PLAYWRIGHT SHOPEE 🔥")
        print("LINK:", link_produto)
        print("===================================")

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            context = await browser.new_context()

            page = await context.new_page()

            page.set_default_timeout(30000)

            # ==========================================
            # ABRE SHOPEE AFILIADOS
            # ==========================================

            await page.goto(
                "https://affiliate.shopee.com.br/",
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(10000)

            print("SHOPEE ABERTA 🔥")

            print(
                "TITULO PAGINA:",
                await page.title()
            )

            # ==========================================
            # ACEITAR COOKIES
            # ==========================================

            try:

                await page.locator(
                    'button:has-text("Aceitar")'
                ).click(
                    force=True,
                    timeout=5000
                )

                print("COOKIES ACEITOS 🔥")

                await page.wait_for_timeout(3000)

            except:

                print("COOKIES JA ACEITOS")

            # ==========================================
            # BOTAO INSERIR
            # ==========================================

            try:

                print("PROCURANDO BOTAO INSERIR 🔥")

                botao_inserir = page.locator(
                    'button:has-text("Inserir")'
                )

                await botao_inserir.wait_for(
                    timeout=15000
                )

                print("BOTAO INSERIR ENCONTRADO 🔥")

                await botao_inserir.click(
                    force=True
                )

                print("BOTAO INSERIR CLICADO 🔥")

                await page.wait_for_timeout(8000)

            except Exception as e:

                print("ERRO BOTAO INSERIR:", e)

                traceback.print_exc()

                await page.screenshot(
                    path="erro_inserir.png",
                    full_page=True
                )

                await client.send_file(
                    "me",
                    "erro_inserir.png",
                    caption="ERRO BOTAO INSERIR 🔥"
                )

                await browser.close()

                return link_produto

            # ==========================================
            # LOGIN
            # ==========================================

            try:

                print("PROCURANDO CAMPO LOGIN 🔥")

                await page.wait_for_selector(
                    'input[type="text"]',
                    timeout=15000
                )

                print("CAMPO LOGIN ENCONTRADO 🔥")

                await page.fill(
                    'input[type="text"]',
                    SHOPEE_LOGIN
                )

                print("LOGIN DIGITADO 🔥")

            except Exception as e:

                print("ERRO CAMPO LOGIN:", e)

                traceback.print_exc()

                await page.screenshot(
                    path="erro_login.png",
                    full_page=True
                )

                await client.send_file(
                    "me",
                    "erro_login.png",
                    caption="ERRO LOGIN SHOPEE 🔥"
                )

                await browser.close()

                return link_produto

            # ==========================================
            # SENHA
            # ==========================================

            try:

                print("PROCURANDO CAMPO SENHA 🔥")

                await page.wait_for_selector(
                    'input[type="password"]',
                    timeout=15000
                )

                print("CAMPO SENHA ENCONTRADO 🔥")

                await page.fill(
                    'input[type="password"]',
                    SHOPEE_SENHA
                )

                print("SENHA DIGITADA 🔥")

            except Exception as e:

                print("ERRO CAMPO SENHA:", e)

                traceback.print_exc()

                await page.screenshot(
                    path="erro_senha.png",
                    full_page=True
                )

                await client.send_file(
                    "me",
                    "erro_senha.png",
                    caption="ERRO SENHA SHOPEE 🔥"
                )

                await browser.close()

                return link_produto

            # ==========================================
            # BOTAO ENTRAR
            # ==========================================

            try:

                print("PROCURANDO BOTAO LOGIN 🔥")

                botao_login = page.locator(
                    'button:has-text("Entrar")'
                ).last

                await botao_login.wait_for(
                    timeout=15000
                )

                print("BOTAO LOGIN ENCONTRADO 🔥")

                await botao_login.click(
                    force=True
                )

                print("BOTAO ENTRAR CLICADO 🔥")

            except Exception as e:

                print("ERRO BOTAO LOGIN:", e)

                traceback.print_exc()

                await page.screenshot(
                    path="erro_botao.png",
                    full_page=True
                )

                await client.send_file(
                    "me",
                    "erro_botao.png",
                    caption="ERRO BOTAO LOGIN 🔥"
                )

                await browser.close()

                return link_produto

            # ==========================================
            # ESPERA LOGIN
            # ==========================================

            await page.wait_for_timeout(15000)

            # ==========================================
            # SCREENSHOT FINAL
            # ==========================================

            await page.screenshot(
                path="03_logado.png",
                full_page=True
            )

            await client.send_file(
                "me",
                "03_logado.png",
                caption="LOGIN SHOPEE REALIZADO 🔥"
            )

            print("LOGIN SHOPEE REALIZADO 🔥")

            await browser.close()

        return link_produto

    except Exception as e:

        print("ERRO PLAYWRIGHT SHOPEE:", e)

        traceback.print_exc()

        try:

            if browser:
                await browser.close()

        except:
            pass

        return link_produto

# ==========================================
# SHEIN
# ==========================================

async def gerar_link_shein(link_produto):

    try:

        print("===================================")
        print("INICIANDO PROCESSAMENTO SHEIN 🔥")
        print("LINK ORIGINAL:", link_produto)
        print("===================================")

        novo_link = link_produto

        print("LINK SHEIN FINAL:", novo_link)

        return novo_link

    except Exception as e:

        print("ERRO SHEIN:", e)

        traceback.print_exc()

        return link_produto

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

            print("SEM TEXTO E SEM FOTO")
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

        # PEGA LINKS
        links = re.findall(
            r"(https?://[^\s]+)",
            texto
        )

        print("LINKS ENCONTRADOS:", links)

        # PROCESSA LINKS
        for i, link in enumerate(links):

            try:

                print("===================================")
                print(f"LINK {i+1}: {link}")
                print("ANALISANDO LINK...")
                print("===================================")

                # MERCADO LIVRE
                if (
                    "mercadolivre" in link.lower()
                    or "meli.la" in link.lower()
                ):

                    print("LINK ML DETECTADO 🔥")

                    novo_link = await gerar_link_afiliado_ml(link)

                    print("LINK NOVO:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # SHOPEE
                elif (

                    "shopee" in link.lower()
                    or "s.shopee.com.br" in link.lower()
                    or "shope.ee" in link.lower()
                    or "shp.ee" in link.lower()

                ):

                    print("LINK SHOPEE DETECTADO 🔥")

                    try:

                        novo_link = await gerar_link_shopee(link)

                    except Exception as e:

                        print("ERRO SHOPEE:", e)

                        traceback.print_exc()

                        novo_link = link

                    print("LINK NOVO SHOPEE:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # SHEIN
                elif (

                    "shein" in link.lower()
                    or "onelink.shein.com" in link.lower()

                ):

                    print("LINK SHEIN DETECTADO 🔥")

                    novo_link = await gerar_link_shein(link)

                    print("LINK NOVO SHEIN:", novo_link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                else:

                    print("LINK NÃO IDENTIFICADO")

                print("FIM PROCESSAMENTO LINK 🔥")

            except Exception as erro_link:

                print("ERRO NO LINK:", erro_link)

                traceback.print_exc()

        print("===================================")
        print("TEXTO FINAL:")
        print(texto)
        print("===================================")

        # FOTO
        if event.photo:

            print("ENVIANDO FOTO 🔥")

            arquivo = await event.download_media()

            await client.send_file(
                canal_destino,
                arquivo,
                caption=texto,
                link_preview=False
            )

        # TEXTO
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

client.run_until_disconnected()