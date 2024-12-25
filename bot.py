import datetime
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram import F
import os
last_time = datetime.datetime.now() - datetime.timedelta(seconds=30)
# Bot tokenini kiriting
API_TOKEN = "7960388262:AAENvlNhoPPnMFu13-mx_IQ12TLVzE0eeb0"

# Bot va Dispatcher yaratish
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# JSON fayl
DATA_FILE = "messages.json"
def load_users():
    if os.path.exists('message.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return {}
           
# Foydalanuvchi xabarlarini json faylga yozish
def save_message_to_json(user_id, message_text):
    try:
        # Faylni ochish yoki yaratish
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Foydalanuvchining xabarlarini yangilash yoki yaratish
    user_id = str(user_id)  # JSON kalitlari faqat string bo'lishi kerak
    if user_id not in data:
        data[user_id] = []
    data[user_id].append(message_text)

    # Ma'lumotlarni yozish
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Xabarni qabul qilish

@dp.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    message_text = message.text
    photo = FSInputFile('foto/ss.jpg')
    if message_text == '/start':
        await bot.send_photo( chat_id=message.chat.id ,photo=photo,caption="""
❗️НАПИШИ В ЧАТ - ПОЛУЧИ СУНДУК

🎁Будет разыграно х10 сундуков ХОЛОДРЫЖЕСТВА (х5 рандомно среди всех участников и х5 самым активным)

1️⃣ Для участие пиши в чат игры (с людьми): «Пасту написал - Аркану залутал: тгк grusti_ne»

Пример предоставлен на скрине☝️

2️⃣ Заходите в этого бота и пишите текст в виде:
 «8095269835 32:22»

8095269835 - ID вашей игры
32:22 - время, в которое вы написали рекламу

❗️КОЛИЧЕСТВО ИГР НЕОГРАНИЧЕНО
""")
    elif message_text == "/uchastniki":
       
        users = load_users()
        g = 0
        for i in users:
            g += 1
        await message.answer(users['6519405204'])
        
    else:
        global last_time
        if (datetime.datetime.now() - last_time).seconds < 30:
            await message.answer("Слишком часто")
            return
        save_message_to_json(user_id, message_text)
        await message.answer("Игра принята и отправлена на обработку\nСледующую игру можете скинуть через 10 минут")
        
@dp.message(F.photo)
async def handle_message(message: Message):
    user_id = message.from_user.id
    message_text = message.caption

    # Xabarni saqlash
    save_message_to_json(user_id, message_text)

    # Javob berish
    await message.answer("dddd")
    await bot.forward_message(chat_id=1002492408975,from_chat_id=user_id,message_id=message.message_id)

# Botni ishga tushirish
async def main():
    # Dispatcherni botga bog'lash
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
