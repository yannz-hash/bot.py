import os
import sys
import asyncio
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== WARNA TERMUX =====
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ===== BANNER =====
def banner():
    os.system("clear")
    print(C + """
╔════════════════════════════════════╗
║     🤖 TELEGRAM DOWNLOADER BOT     ║
║   TikTok & Instagram • No WM      ║
╚════════════════════════════════════╝
""" + W)

# ===== INPUT TOKEN =====
def input_token():
    token = input(Y + "Masukkan token bot: " + W).strip()
    if not token:
        print(R + "Token tidak boleh kosong!" + W)
        sys.exit()
    return token

# ===== PROGRESS BAR =====
def progress_bar(p):
    bars = int(p / 20)
    return "▰" * bars + "▱" * (5 - bars)

# ===== /START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *BOT AKTIF*\n\n"
        "📥 Kirim link *TikTok / Instagram*\n"
        "📌 Bisa banyak link sekaligus\n"
        "🚀 Tanpa watermark",
        parse_mode="Markdown"
    )

# ===== DOWNLOAD =====
async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = update.message.text.strip().splitlines()

    for link in links:
        if not ("tiktok.com" in link or "instagram.com" in link):
            await update.message.reply_text(f"❌ Link tidak didukung:\n{link}")
            continue

        msg = await update.message.reply_text("⏳ Downloading...\n▱▱▱▱▱ 0%")

        for p in [25, 50, 75]:
            await asyncio.sleep(1)
            await msg.edit_text(
                f"⏳ Downloading...\n{progress_bar(p)} {p}%"
            )

        subprocess.run(
            ["yt-dlp", "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s", link],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        files = os.listdir(DOWNLOAD_DIR)
        if not files:
            await update.message.reply_text("❌ Gagal download")
            return

        video_path = os.path.join(DOWNLOAD_DIR, files[0])
        await msg.edit_text(f"✅ Selesai!\n{progress_bar(100)} 100%")
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)

# ===== MAIN =====
def main():
    banner()
    TOKEN = input_token()

    print(Y + "[*] Mengecek token..." + W)
    try:
        app = ApplicationBuilder().token(TOKEN).build()
    except:
        print(R + "[X] TOKEN TIDAK VALID!" + W)
        sys.exit()

    print(G + "[✓] TOKEN VALID — BOT AKTIF" + W)
    print(C + "[i] CTRL+C untuk keluar\n" + W)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))
    app.run_polling()

if __name__ == "__main__":
    main()
