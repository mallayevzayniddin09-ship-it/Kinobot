import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests
import pickle

BOT_TOKEN = '7805028417:AAHK9C4QwNnBSImdOI-B77MZ_ZJdrAcSMWM'
ADMIN_ID = 6857712473
CHANNEL_USERNAME = '@fcmobile_uz_savdo'
KINOLAR_FILE = 'kinolar.pkl'

def load_kinolar():
    if os.path.exists(KINOLAR_FILE):
        with open(KINOLAR_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_kinolar(kinolar):
    with open(KINOLAR_FILE, 'wb') as f:
        pickle.dump(kinolar, f)

async def check_subscription(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    data = requests.get(url).json()
    status = data.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Kino raqamini yozing yoki admin bo‘lsangiz videoga reply qilib raqam yuboring."
    )

async def add_kino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Sizda kino qo‘shish uchun ruxsat yo‘q!")
        return

    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        await update.message.reply_text("Kino qo‘shish uchun videoga reply qilib raqam yozing!")
        return

    try:
        kino_num = int(update.message.text)
        video_file_id = update.message.reply_to_message.video.file_id
        kinolar = load_kinolar()
        kinolar[kino_num] = video_file_id
        save_kinolar(kinolar)
        await update.message.reply_text(f"Kino {kino_num}-raqamga saqlandi!")
    except Exception:
        await update.message.reply_text("Xato: faqat raqam yozing va videoga reply qiling.")

async def send_kino(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not await check_subscription(user_id):
        await update.message.reply_text(f"Kino olish uchun {CHANNEL_USERNAME} kanaliga obuna bo‘ling!")
        return

    try:
        kino_num = int(update.message.text)
        kinolar = load_kinolar()
        video_file_id = kinolar.get(kino_num)
        if video_file_id:
            await update.message.reply_video(video=video_file_id, caption=f"Kino raqami: {kino_num}")
        else:
            await update.message.reply_text("Bunday raqamda kino topilmadi.")
    except:
        await update.message.reply_text("Faqat raqam yozing yoki admin bo‘lsangiz videoga reply qilib raqam yuboring!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.REPLY, add_kino))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_kino))
    app.run_polling()

if __name__ == "__main__":
    main()