# =============================================================================
# config.py — Bot sozlamalarini yuklash
# =============================================================================
#
# Bu faylning vazifasi: bot tokeni va boshqa maxfiy ma'lumotlarni KODDAN AJRATIB
# .env faylidan o‘qish. Nima uchun kerak?
#   - Token kodda bo‘lsa, GitHub/forumga yuborganingizda o‘gri ishlatishi mumkin.
#   - .env faylini .gitignore ga qo‘shsak, token hech qachon omborga kirmaydi.
#   - Har bir dasturchi o‘z .env faylini yaratadi, bitta kod hammaga yaxshi.
#
# =============================================================================

import os
# os — operatsion tizim bilan ishlash (muhit o‘zgaruvchilarini o‘qish uchun).

from dotenv import load_dotenv
# load_dotenv — .env faylini o‘qiydi va BOT_TOKEN kabi o‘zgaruvchilarni
# xotirada (os.environ) mavjud qiladi. Shundan keyin os.getenv() ishlaydi.


# load_dotenv() ni chaqirish — loyiha papkasidagi .env faylini topib,
# ichidagi BOT_TOKEN=... kabi qatorlarni o‘qiydi va ularni muhit o‘zgaruvchilari
# sifatida qo‘yadi. Bu funksiyani dastur boshida bir marta chaqirish kifoya.
load_dotenv()


# BOT_TOKEN — BotFather bergan maxfiy kalit. Bot Telegram serveriga shu orqali
# «bu men» deb tanishtiradi. os.getenv("BOT_TOKEN", "") degani: "BOT_TOKEN" nomli
# muhit o‘zgaruvchisini o‘qi; agar yo‘q bo‘lsa, "" (bo‘sh qator) qaytar.
# Ikkinchi argument ("") — default qiymat.
BOT_TOKEN = os.getenv("BOT_TOKEN", "")


def get_token():
    """
    Bot tokenini qaytaradi va bo‘sh emasligini tekshiradi.
    Ishga tushirish uchun: bot.py bu funksiyani chaqirib tokenni oladi.
    Agar .env da BOT_TOKEN bo‘lmasa yoki bo‘sh qator bo‘lsa — ValueError
    chiqarib, dastur to‘xtaydi (tokensiz bot ishlamaydi).
    """
    # strip() — bosh va oxiridagi bo‘shliq/tab larni olib tashlaydi.
    # Masalan: "  abc  " -> "abc". Foydalanuvchi .env da ortiqcha probel
    # qoldirsa ham, token to‘g‘ri ishlaydi.
    token = BOT_TOKEN.strip()

    # Agar token bo‘sh qator bo‘lsa (""), not token True bo‘ladi.
    # Bu holda ishga tushirish mantiqan xato — xabarni chiqaramiz va
    # dasturni to‘xtatamiz (raise = xato «otkazish»).
    if not token:
        raise ValueError(
            "BOT_TOKEN topilmadi! .env faylini yarating va BOT_TOKEN=tokeningiz qo‘shing"
        )

    return token
