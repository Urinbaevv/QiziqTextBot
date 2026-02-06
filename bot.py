# =============================================================================
# bot.py — Loyihaning kirish nuqtasi (entry point)
# =============================================================================
#
# Bu faylni ishga tushirsak (python bot.py), bot yoqiladi va Telegram dan
# xabarlarni kutadi. Boshqa fayllar faqat import qilinadi: config dan token,
# handlers dan router. Asosiy mantiq shu yerdan boshlanadi.
#
# Asosiy tushunchalar:
#   - Bot — Telegram API bilan muloqot (xabar yuborish, qabul qilish).
#   - Dispatcher (dp) — kelgan yangilanishlarni (xabar, tugma bosish va h.k.)
#     qaysi handler ga yuborishni hal qiladi.
#   - Router — handlerlar to‘plami. dp.include_router(router) = «router dagi
#     barcha handlerlarni ulab qo‘y».
#   - start_polling — bot Telegram serveriga doim «yangi xabar bormi?» deb
#     so‘raydi (long polling). Xabar kelsa — handler chaqiladi.
#
# =============================================================================

import asyncio
# asyncio — asinxron dasturlash. aiogram 3 async/await dan foydalanadi:
# bir nechta foydalanuvchi bir vaqtda xabar yuborganida ham bot javob bera oladi.

import logging
# logging — konsolga yozuv chiqarish (xatoliklar, yangilanishlar). Bot ishlaganda
# «INFO: ...» ko‘rasiz — qaysi xabar qayta ishlanganini kuzatish oson.

from aiogram import Bot, Dispatcher
# Bot — Telegram bot ob’ekti. Token orqali yaratiladi.
# Dispatcher — yangilanishlarni handlerlarga yo‘naltiradi.

from config import get_token
# get_token() — .env dan BOT_TOKEN ni o‘qiydi va bo‘sh emasligini tekshiradi.
# Token bo‘lmasa ValueError chiqadi, dastur to‘xtaydi.

from handlers import router
# router — handlers.py da yaratilgan Router. Unda cmd_start va handle_text
# kabi handlerlar ro‘yxatdan o‘tgan. Shu router ni dp ga ulaymiz.


# logging.basicConfig — barcha log xabarlarini sozlash. level=logging.INFO
# degani: INFO va undan muhimroq (WARNING, ERROR) xabarlar konsolga chiqadi.
# Bot ishga tushganda va xabar qayta ishlanganda ko‘rishingiz mumkin.
logging.basicConfig(level=logging.INFO)


async def main():
    """
    Asosiy funksiya: botni yaratish, router ulash va long polling ishga tushirish.
    async — bu funksiya asinxron; await bilan boshqa async funksiyalarni
    chaqirishimiz mumkin (masalan start_polling).
    """
    # Token ni config dan olamiz. Bu yerda xato chiqsa (token yo‘q), dastur
    # to‘xtaydi — get_token() ichida raise ValueError bor.
    token = get_token()

    # Bot ob’ektini yaratamiz. Token — BotFather bergan maxfiy kalit.
    bot = Bot(token=token)

    # Dispatcher — «dispetcher»: kelgan xabarlarni handlerlarga taqsimlaydi.
    # Yangi Dispatcher yaratamiz, hali hech qanday handler ulanmagan.
    dp = Dispatcher()

    # handlers.py dagi router ni ulaymiz. Router ichida Command("start") va
    # F.text bo‘yicha handlerlar bor. Endi foydalanuvchi /start yoki matn
    # yuborganida dp shu handlerlarni chaqiradi.
    dp.include_router(router)

    # start_polling(bot) — bot Telegram serveriga ulanishni boshlaydi va doim
    # yangilanishlarni so‘raydi (long polling). Xabar kelsa — dp tegishli
    # handler ni chaqadi. await — bu jarayon to‘xtaguncha (Ctrl+C gacha) dastur
    # shu yerdan davom etadi.
    await dp.start_polling(bot)


# __name__ == "__main__" — bu fayl to‘g‘ridan-to‘g‘ri ishga tushirilganda
# (python bot.py). Import qilinganda (boshqa fayldan import bot) main() chaqilmaydi.
# asyncio.run(main()) — main() ni asinxron ishga tushiradi; to‘xtaguncha kutadi.
#
# KeyboardInterrupt — foydalanuvchi botni to‘xtatish uchun Ctrl+C (yoki terminalda
# «Stop») bosganda Python chiqaradigan maxsus «xato». Aslida bu xato emas, balki
# «dasturni to‘xtatish» buyrug‘i. Agar uni ushlamasak, konsolda uzun traceback
# (xato matni) chiqadi va o‘quvchiga chalkash tuyuladi. try/except orqali ushlab,
# oddiy xabar chiqaramiz va dasturni tinch yopamiz.
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl+C bosilganda shu blok bajariladi. Bot to‘xtatiladi, xato matni
        # chiqmaydi — faqat quyidagi xabar va dastur 0 kod bilan tugaydi.
        print("\nBot to‘xtatildi. (Ctrl+C)")
