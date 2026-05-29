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

# SHOPEE
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
        print("LINK SHOPEE DETECTADO 🔥")
        print("LINK:", link_produto)
        print("===================================")

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = await browser.new_context(

                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),

                viewport={
                    "width": 1366,
                    "height": 768
                },

                locale="pt-BR",

                timezone_id="America/Sao_Paulo"
            )

            page = await context.new_page()

            # ==========================================
            # STEALTH
            # ==========================================

            await page.add_init_script("""

            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });

            window.chrome = {
                runtime: {},
            };

            Object.defineProperty(navigator, 'languages', {
                get: () => ['pt-BR', 'pt'],
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            """)

            page.set_default_timeout(30000)

            # ==========================================
            # LOGIN PAGE
            # ==========================================

            await page.goto(
                "https://affiliate.shopee.com.br/login",
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("PAGINA LOGIN ABERTA 🔥")

            await page.wait_for_timeout(5000)

            # ==========================================
            # LOGIN
            # ==========================================

            await page.wait_for_selector(
                'input[type="text"]',
                timeout=15000
            )

            await page.fill(
                'input[type="text"]',
                SHOPEE_LOGIN
            )

            print("LOGIN DIGITADO 🔥")

            # ==========================================
            # SENHA
            # ==========================================

            await page.wait_for_selector(
                'input[type="password"]',
                timeout=15000
            )

            await page.fill(
                'input[type="password"]',
                SHOPEE_SENHA
            )

            print("SENHA DIGITADA 🔥")

            # ==========================================
            # BOTAO LOGIN
            # ==========================================

            await page.wait_for_selector(
                "button",
                timeout=30000
            )

            print("BOTOES CARREGADOS 🔥")

            botoes = page.locator("button")

            total = await botoes.count()

            print(f"TOTAL BOTOES: {total}")

            clicou = False

            for i in range(total):

                try:

                    botao = botoes.nth(i)

                    texto_botao = await botao.inner_text()

                    print(f"BOTAO {i}: {texto_botao}")

                    if (
                        "entrar" in texto_botao.lower()
                        or "login" in texto_botao.lower()
                    ):

                        print("BOTAO LOGIN ENCONTRADO 🔥")

                        await botao.click(
                            force=True
                        )

                        print("BOTAO LOGIN CLICADO 🔥")

                        clicou = True

                        break

                except:
                    pass

            if not clicou:

                print("BOTAO LOGIN NAO ENCONTRADO ❌")

                await browser.close()

                return link_produto

            # ==========================================
            # ESPERA LOGIN
            # ==========================================

            await page.wait_for_timeout(10000)

            print("LOGIN REALIZADO 🔥")

            # ==========================================
            # ABRE LINK PRODUTO
            # ==========================================

            await page.goto(
                link_produto,
                wait_until="domcontentloaded",
                timeout=60000
            )

            print("LINK PRODUTO ABERTO 🔥")

            await page.wait_for_timeout(10000)

            # ==========================================
            # PEGA LINK FINAL
            # ==========================================

            novo_link = page.url

            print("LINK NOVO SHOPEE:", novo_link)

            await browser.close()

            return novo_link

    except Exception as e:

        print("ERRO SHOPEE:", e)

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
        print("LINK SHEIN ORIGINAL 🔥")
        print(link_produto)
        print("===================================")

        return link_produto

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

                if (
                    "mercadolivre" in link.lower()
                    or "meli.la" in link.lower()
                ):

                    print("LINK ML DETECTADO 🔥")

                    novo_link = await gerar_link_afiliado_ml(link)

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # ==========================================
                # SHOPEE
                # ==========================================

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

                    texto = re.sub(
                        re.escape(link),
                        novo_link,
                        texto
                    )

                # ==========================================
                # SHEIN
                # ==========================================

                elif (

                    "shein" in link.lower()
                    or "onelink.shein.com" in link.lower()

                ):

                    print("LINK SHEIN DETECTADO 🔥")

                    novo_link = await gerar_link_shein(link)

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

        # ==========================================
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