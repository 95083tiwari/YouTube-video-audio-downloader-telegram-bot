from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import yt_dlp
import glob
import os

CHANNEL_MSG = "\n\n❤️ Please join our channel: @lifeonbots"

# =========================
# START COMMAND
# =========================
def start(update, context):
    update.message.reply_text(
        "👋 Welcome! YouTube Video & Audio Downloader Bot.\n\n👇 Link bhejo...",
    )

# =========================
# HANDLE YOUTUBE LINK
# =========================
def handle_message(update, context):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        update.message.reply_text("❌ YouTube ka link bhejo!")
        return

    context.user_data["url"] = url

    keyboard = [
        [InlineKeyboardButton("🎧 Audio (MP3)", callback_data="audio")],
        [InlineKeyboardButton("📹 144p", callback_data="144")],
        [InlineKeyboardButton("📹 240p", callback_data="240")],
        [InlineKeyboardButton("📹 360p", callback_data="360")],
        [InlineKeyboardButton("📹 480p", callback_data="480")],
        [InlineKeyboardButton("📹 720p", callback_data="720")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "👇 Please select quality:" + CHANNEL_MSG,
        reply_markup=reply_markup
    )

# =========================
# BUTTON HANDLER
# =========================
def button(update, context):
    query = update.callback_query
    query_data = query.data
    url = context.user_data.get("url")

    query.answer()
    query.edit_message_text("⏳ Downloading... Please wait..." + CHANNEL_MSG)

    # DOWNLOAD OPTIONS
    if query_data == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }
    else:
        ydl_opts = {
            "format": f"bestvideo[height<={query_data}]+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
        }

    try:
        # DOWNLOAD
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # FIND NEWEST FILE
        files = glob.glob("*.mp4") + glob.glob("*.mp3")
        files.sort(key=os.path.getmtime)
        file_path = files[-1]

        # SEND FILE
        if file_path.endswith(".mp3"):
            query.message.reply_audio(audio=open(file_path, "rb"), caption=CHANNEL_MSG)
        else:
            query.message.reply_video(video=open(file_path, "rb"), caption=CHANNEL_MSG)

        os.remove(file_path)

    except:
        query.message.reply_text("❌ Error! Link sahi hai ya video private to nahi?" + CHANNEL_MSG)


# =========================
# MAIN
# =========================
def main():
    updater = Updater("YOUR_BOT_TOKEN_HERE", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
