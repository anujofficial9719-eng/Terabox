import os
import re
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

TERABOX_REGEX = r'https?://.*(terabox|1024terabox).*'

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# --------- Direct Link Extractor (API) ---------

def get_direct_link(url):

    api = f"https://terabox-dl-api.vercel.app/api?url={url}"

    r = requests.get(api).json()

    if "download_url" in r:
        return r["download_url"]

    raise Exception("Direct link not found")


# --------- Download Video ---------

def download_video(url):

    local_file = os.path.join(DOWNLOAD_FOLDER, "video.mp4")

    with requests.get(url, stream=True) as r:

        with open(local_file, "wb") as f:

            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

    return local_file


# --------- Commands ---------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Send Terabox link\nI will upload the video here."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if not re.match(TERABOX_REGEX, url):

        await update.message.reply_text("❌ Send valid Terabox link")
        return

    msg = await update.message.reply_text("⏳ Fetching video...")

    try:

        direct = get_direct_link(url)

        await msg.edit_text("⬇ Downloading video...")

        file_path = download_video(direct)

        await msg.edit_text("⬆ Uploading to Telegram...")

        await update.message.reply_video(
            video=open(file_path, "rb"),
            caption="✅ Uploaded from Terabox"
        )

        os.remove(file_path)

        await msg.delete()

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error : {str(e)}"
        )


# --------- Main ---------

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT, handle_link))

    logger.info("Bot Running")

    await app.run_polling()


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
