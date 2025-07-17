# handlers.py

from aiogram import types
from config import ADMIN_ID, CHANNEL_ID, MOVIES

# Obuna tekshirish funksiyasi
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# /start komandasi
async def handle_start(message: types.Message, bot):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(bot, user_id)

    if is_subscribed:
        await message.answer("👋 Salom! Kino olish uchun raqam yuboring. Masalan: 1, 2, 3 ...")
    else:
        link = f"https://t.me/{str(CHANNEL_ID).replace('-100', '')}"
        await message.answer(
            f"📢 Kino ko‘rish uchun quyidagi kanalga obuna bo‘ling:\n\n👉 {link}",
            disable_web_page_preview=True
        )

# Raqam yuborilganda
async def handle_other_messages(message: types.Message, bot):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text.isdigit():
        await message.reply("❗ Faqat raqam yuboring. Masalan: 1")
        return

    is_subscribed = await check_subscription(bot, user_id)
    if not is_subscribed:
        link = f"https://t.me/{str(CHANNEL_ID).replace('-100', '')}"
        await message.answer(f"🚫 Avval kanalga obuna bo‘ling:\n👉 {link}")
        return

    movie = MOVIES.get(text)
    if movie:
        await message.answer_video(video=movie, caption=f"🎬 Kino {text}")
    else:
        await message.reply("❌ Bunday raqamdagi kino yo‘q.")
