import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TG_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Gửi link Douyin cho mình, mình sẽ tải video cho bạn!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "douyin.com" not in url:
        await update.message.reply_text("❌ Đây không phải link Douyin.")
        return

    await update.message.reply_text("⏳ Đang tải video...")

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open("video.mp4", "rb"))
        os.remove("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()

if __name__ == "__main__":
    main()