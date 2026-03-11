import os
import re
import time
import logging
import requests
from urllib.parse import urlparse, parse_qs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

====== 🇮🇳 ==============

# © Developer = Anuj Kumar

========================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Telegram bot token (set as environment variable for safety)

TELEGRAM_BOT_TOKEN = os.environ.get("8726665578:AAHLSN3AxqWoRzeSJU2oV4Bm4QPfKKSkPKo")

Supported domains

SUPPORTED_DOMAINS = [
"terabox.com",
"1024terabox.com",
"teraboxapp.com",
"teraboxlink.com",
"terasharelink.com",
"terafileshare.com",
"www.1024tera.com",
"1024tera.com",
"1024tera.cn",
"teraboxdrive.com",
"dubox.com"
]

TERABOX_URL_REGEX = r'^https://(www.)?(terabox.com|1024terabox.com|teraboxapp.com|teraboxlink.com|terasharelink.com|terafileshare.com|1024tera.com|1024tera.cn|teraboxdrive.com|dubox.com)/(s|sharing/link)/[A-Za-z0-9_-]+'

Tested cookies (same as Flask API)

COOKIES = {
'ndut_fmt': '082E0D57C65BDC31F6FF293F5D23164958B85D6952CCB6ED5D8A3870CB302BE7',
'ndus': 'Y-wWXKyteHuigAhC03Fr4bbee-QguZ4JC6UAdqap',
'__bid_n': '196ce76f980a5dfe624207',
'__stripe_mid': '148f0bd1-59b1-4d4d-8034-6275095fc06f99e0e6',
'__stripe_sid': '7b425795-b445-47da-b9db-5f12ec8c67bf085e26',
'browserid': 'veWFJBJ9hgVgY0eI9S7yzv66aE28f3als3qUXadSjEuICKF1WWBh4inG3KAWJsAYMkAFpH2FuNUum87q',
'csrfToken': 'wlv_WNcWCjBtbNQDrHSnut2h',
'lang': 'en',
'PANWEB': '1',
'ab_sr': '1.0.1_NjA1ZWE3ODRiYjJiYjZkYjQzYjU4NmZkZGVmOWYxNDg4MjU3ZDZmMTg0Nzg4MWFlNzQzZDMxZWExNmNjYzliMGFlYjIyNWUzYzZiODQ1Nzg3NWM0MzIzNWNiYTlkYTRjZTc0ZTc5ODRkNzg4NDhiMTljOGRiY2I4MzY4ZmYyNTU5ZDE5NDczZmY4NjJhMDgyNjRkZDI2MGY5M2Q5YzIyMg=='
}

HEADERS = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1'
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

---------------- Helper Functions ----------------

def validate_terabox_url(url):
"""Validate Terabox URL format"""
try:
return re.match(TERABOX_URL_REGEX, url) is not None
except Exception:
return False

def make_request(url, method='GET', headers=None, params=None, allow_redirects=True, cookies=None):
"""Make HTTP request with retry logic"""
session = requests.Session()
retries = 0
last_exception = None

while retries < MAX_RETRIES:  
    try:  
        response = session.request(  
            method,  
            url,  
            headers=headers or HEADERS,  
            params=params,  
            cookies=cookies,  
            allow_redirects=allow_redirects,  
            timeout=REQUEST_TIMEOUT  
        )  
        if response.status_code in [403, 429, 503]:  
            time.sleep(RETRY_DELAY * (2 ** retries))  
            retries += 1  
            continue  
        response.raise_for_status()  
        return response  
    except (requests.ConnectionError, requests.Timeout) as e:  
        time.sleep(RETRY_DELAY * (2 ** retries))  
        retries += 1  
        last_exception = e  
    except requests.RequestException as e:  
        if retries == MAX_RETRIES - 1:  
            raise  
        time.sleep(RETRY_DELAY)  
        retries += 1  
        last_exception = e  
raise Exception(f"Max retries exceeded. Last error: {str(last_exception)}")

Here you can reuse all your extract_tokens, get_surl, process_terabox_url

and get_direct_link functions as they are from your Flask code.

---------------- Telegram Bot Handlers ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"👋 Welcome! Send me a Terabox link, and I will fetch the files for you.\n"
"Usage: Just send a URL like https://terabox.com/s/xxxx"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text.strip()

if not validate_terabox_url(url):  
    await update.message.reply_text(  
        "❌ Invalid Terabox URL.\n"  
        f"Supported domains: {', '.join(SUPPORTED_DOMAINS)}"  
    )  
    return  
  
await update.message.reply_text("⏳ Processing your Terabox link, please wait...")  
  
try:  
    files = process_terabox_url(url)  
    if not files:  
        await update.message.reply_text("❌ No files found in this link.")  
        return  
      
    for file in files:  
        text = (  
            f"📄 Name: {file['file_name']}\n"  
            f"💾 Size: {file['size']}\n"  
            f"🔗 Download: {file['direct_download_url']}"  
        )  
        await update.message.reply_text(text)  
          
except Exception as e:  
    await update.message.reply_text(f"❌ Error processing link: {str(e)}")

---------------- Run the Bot ----------------

async def main():
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))  
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))  
  
logger.info("Bot is running...")  
await app.run_polling()

if name == "main":
import asyncio
asyncio.run(main())
