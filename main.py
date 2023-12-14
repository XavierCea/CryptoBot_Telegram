from telegram.ext import *
from telegram import *
from keys import USERNAME, API_KEY
from bs4 import BeautifulSoup
import requests


async def start_command(update: Update, context: ContextTypes):
    """Return to the user a welcome message to notice that works"""
    await update.message.reply_text('Bienvenido a Cegon CryptoBot!')

async def crypto_command(update: Update, context: ContextTypes):
    """Read the user input and if the crypto exist, get the actual value in Euros and response to the user"""
    crypto = update.message.text.replace("/crypto", "")
    crypto = " ".join(crypto.split())
    try:
        crypto_search = crypto.replace(" ", "-")
        url = requests.get(f'https://awebanalysis.com/es/coin-details/{crypto_search}/EUR/')
        soup = BeautifulSoup(url.content, 'html.parser')
        result = soup.find('td', {'class': 'text-larger text-price'})
        await update.message.reply_text(f"El precio de {crypto} es de {result.text}")
    except:
        await update.message.reply_text(f"La crypto {crypto} no existe o no se encuentra")


if __name__ == '__main__':
    print("Iniciando bot...")
    app = Application.builder().token(API_KEY).build()

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('crypto',crypto_command))

    print("Bot Iniciado")

    app.run_polling(poll_interval=1, timeout=10)
