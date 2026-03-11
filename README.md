📦 TeraBox Downloader Telegram Bot

A simple Telegram Bot that extracts direct download links from TeraBox share URLs.

This bot allows users to send a TeraBox link and receive the file name, size, and direct download link instantly.

---

🚀 Features

- 📥 Extract files from TeraBox share links
- ⚡ Fast processing with retry system
- 🔗 Direct download links
- 📄 Shows file name and size
- 🌐 Supports multiple TeraBox domains

---

🌍 Supported Domains

The bot supports the following domains:

- terabox.com
- 1024terabox.com
- teraboxapp.com
- teraboxlink.com
- terasharelink.com
- terafileshare.com
- 1024tera.com
- 1024tera.cn
- teraboxdrive.com
- dubox.com

---

🛠 Requirements

Install the required Python libraries:

pip install python-telegram-bot requests

---

⚙️ Environment Variables

For security, store your Telegram Bot Token as an environment variable.

TELEGRAM_BOT_TOKEN=your_bot_token_here

---

▶️ Run the Bot

Run the bot using:

python main.py

The bot will start and listen for messages.

---

🤖 Bot Usage

1. Start the bot on Telegram.
2. Send the "/start" command.
3. Send a TeraBox share link.

Example:

https://terabox.com/s/xxxxx

The bot will reply with:

- 📄 File Name
- 💾 File Size
- 🔗 Direct Download Link

---

📂 Project Structure

project
│
├── main.py
├── README.md
└── requirements.txt

---

📌 Notes

- Make sure your cookies are valid for TeraBox requests.
- If cookies expire, you may need to update them.

---

👨‍💻 Developer

Anuj Kumar 🇮🇳

---

⚠️ Disclaimer

This bot is created for educational purposes only.
Use it responsibly and follow TeraBox terms of service.

---
