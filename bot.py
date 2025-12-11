from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pytube import YouTube

⬇️⬇️ YAHAN TOKEN PASTE KARNA HAI BAS ⬇️⬇️

TOKEN = "8289235946:AAFWf7ZC-59jHDT5UI78k04meDa1LcRxCfE"

PROMO = "\n\n📢 Please join our channel: @lifeonbots"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
msg = (
"👋 Welcome to YouTube Downloader Bot!\n\n"
"📌 YouTube link bhejo, bot video/audio dono de dega.\n"
"🔥 Fast & HD Downloader\n"
f"{PROMO}"
)
await update.message.reply_text(msg, parse_mode="Markdown")

async def handle_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text

if "youtube.com" not in url and "youtu.be" not in url:  
    await update.message.reply_text("❌ Please send a valid YouTube URL.")  
    return  

await update.message.reply_text("⏳ Downloading... Please wait...")  

try:  
    yt = YouTube(url)  
    title = yt.title  

    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()  
    video_path = video_stream.download(filename="video.mp4")  

    audio_stream = yt.streams.filter(only_audio=True).first()  
    audio_path = audio_stream.download(filename="audio.mp3")  

    await update.message.reply_video(  
        video=open("video.mp4", "rb"),  
        caption=f"🎬 **Video:** {title}{PROMO}",  
        parse_mode="Markdown"  
    )  

    await update.message.reply_audio(  
        audio=open("audio.mp3", "rb"),  
        caption=f"🎵 **Audio:** {title}{PROMO}",  
        parse_mode="Markdown"  
    )  

except Exception as e:  
    await update.message.reply_text("❌ Error! Download nahi ho paya.")  
    print(e)

def main():
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))  
app.add_handler(MessageHandler(filters.TEXT, handle_youtube))  

print("Bot Started...")  
app.run_polling()

if name == "main":
main()
