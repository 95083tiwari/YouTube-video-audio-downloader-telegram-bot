# ========= BOT CONFIG (YAHI TOKEN DAALO) =========
BOT_TOKEN = "8049358854:AAFmNKd6sbfjq7AQsZIa9OPPFksiOcc40qo"  # <-- Apna bot token yaha paste karo
CHANNEL_TEXT = "\n\n🔔 Join our Channel @lifeonbots"
# ===============================================

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import yt_dlp

DOWNLOAD_PATH = "downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 YouTube link bhejo (video / audio download ke liye)." + CHANNEL_TEXT
    )

# YouTube link handler
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    context.user_data['url'] = url

    keyboard = [
        [InlineKeyboardButton("🎬 Video 360p", callback_data="v_360"),
         InlineKeyboardButton("🎬 Video 720p", callback_data="v_720")],
        [InlineKeyboardButton("🎬 Video 1080p", callback_data="v_1080")],
        [InlineKeyboardButton("🎧 Audio MP3", callback_data="audio")]
    ]

    await update.message.reply_text(
        "👇 Quality choose karo:" + CHANNEL_TEXT,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button click handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get('url')
    choice = query.data

    await query.edit_message_text("⏳ Download ho raha hai..." + CHANNEL_TEXT)

    # Audio option
    if choice == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        res = choice.split('_')[1]
        ydl_opts = {
            'format': f'bestvideo[height<={res}]+bestaudio/best/best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4'
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        if choice == "audio":
            file_path = file_path.replace('.webm', '.mp3').replace('.m4a', '.mp3')

    # File size check (MB)
    file_size = os.path.getsize(file_path) / (1024 * 1024)

    # Large file = document
    if file_size > 49:
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=open(file_path, 'rb'),
            caption="📁 Large file (Document mode)" + CHANNEL_TEXT
        )
    else:
        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=open(file_path, 'rb'),
            caption="✅ Download Complete" + CHANNEL_TEXT
        )

    os.remove(file_path)

# Main runner
def main():
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ ERROR: Bot token add nahi kiya")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot successfully start ho gaya")
    app.run_polling()

if __name__ == '__main__':
    main()
