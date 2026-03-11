import os
import re
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

COOKIES = {
    "ndus": "Y-wWXKyteHuigAhC03Fr4bbee-QguZ4JC6UAdqap",
    "lang": "en",
    "PANWEB": "1"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.terabox.com/"
}

# -------- Extract surl --------

def get_surl(url):
    match = re.search(r'/s/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)

# -------- Get files --------

def get_files(url):

    surl = get_surl(url)

    api = "https://www.terabox.com/share/list"

    params = {
        "app_id": "250528",
        "shorturl": surl,
        "root": "1"
    }

    r = requests.get(api, params=params, cookies=COOKIES, headers=HEADERS, timeout=20)

    data = r.json()

    if "list" not in data:
        raise Exception("❌ Invalid link or cookies expired")

    return data["list"]

# -------- Download --------

def download_file(link, filename):

    path = os.path.join(DOWNLOAD_FOLDER, filename)

    with requests.get(link, stream=True) as r:
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

    return path

# -------- Telegram commands --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Send Terabox link\nBot will upload video here."
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    if "terabox" not in url:

        await update.message.reply_text("❌ Send valid Terabox link")
        return

    msg = await update.message.reply_text("🔍 Fetching file...")

    try:

        files = get_files(url)

        for f in files:

            name = f["server_filename"]
            link = f["dlink"]

            await msg.edit_text("⬇ Downloading...")

            file_path = download_file(link, name)

            await msg.edit_text("⬆ Uploading...")

            await update.message.reply_video(
                video=open(file_path, "rb"),
                caption=name
            )

            os.remove(file_path)

        await msg.delete()

    except Exception as e:

        await update.message.reply_text(str(e))


# -------- Main --------

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_link))

    logger.info("Bot Running...")

    await app.run_polling()


if __name__ == "__main__":

    import asyncio
    asyncio.run(main())
