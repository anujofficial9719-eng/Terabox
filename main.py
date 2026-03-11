import os
import re
import time
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ---------------- LOGGING ----------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- BOT TOKEN ----------------

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ---------------- SUPPORTED DOMAINS ----------------

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

TERABOX_URL_REGEX = r'^https://(www\.)?(terabox\.com|1024terabox\.com|teraboxapp\.com|teraboxlink\.com|terasharelink\.com|terafileshare\.com|1024tera\.com|1024tera\.cn|teraboxdrive\.com|dubox\.com)/(s|sharing/link)/[A-Za-z0-9_-]+'

# ---------------- HELPER ----------------

def validate_terabox_url(url):
    try:
        return re.match(TERABOX_URL_REGEX, url) is not None
    except:
        return False


# ---------------- SIMPLE TERABOX PARSER ----------------

def process_terabox_url(url):
    
    # Demo response (आप यहाँ अपना API लगा सकते हो)
    
    return [
        {
            "file_name": "Sample Video",
            "size": "100 MB",
            "direct_download_url": url
        }
    ]


# ---------------- BOT COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me a Terabox link.\n"
        "Example:\n"
        "https://terabox.com/s/xxxx"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if not validate_terabox_url(url):

        await update.message.reply_text(
            "❌ Invalid Terabox URL.\n"
            f"Supported domains:\n{', '.join(SUPPORTED_DOMAINS)}"
        )
        return

    msg = await update.message.reply_text(
        "⏳ Processing your Terabox link..."
    )

    try:

        files = process_terabox_url(url)

        if not files:

            await msg.edit_text("❌ No files found.")
            return

        for file in files:

            text = (
                f"📄 Name : {file['file_name']}\n"
                f"💾 Size : {file['size']}\n"
                f"🔗 Download : {file['direct_download_url']}"
            )

            await update.message.reply_text(text)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error processing link:\n{str(e)}"
        )


# ---------------- MAIN ----------------

async def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    )

    logger.info("Bot Running...")

    await app.run_polling()


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
