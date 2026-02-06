# =============================================================================
# keyboards.py — Bot klaviaturalari
# =============================================================================
#
# Klaviatura — foydalanuvchi ko‘radigan tugmalar (masalan: «Yordam», «Namuna»).
# Bu loyihada foydalanuvchi oddiygina matn yozadi, tugmalar majburiy emas.
# Fayl loyiha tuzilishiga moslash uchun qoldirilgan va kelajakda tugma qo‘shish
# uchun namuna (commentda) keltirilgan.
#
# Qachon kerak bo‘ladi?
#   - «Namuna matn» tugmasi — bir bosishda "Hello" yoki "Salom" yuborish.
#   - «Yordam» tugmasi — /start dagi ma'lumotni qayta ko‘rsatish.
#   - Boshqa menyu tugmalari — bot funksiyalarini kengaytirsangiz.
#
# Qanday ishlatish (qo‘shmoqchi bo‘lsangiz):
#   1. ReplyKeyboardMarkup va KeyboardButton import qiling (pastdagi comment
#      ochilsa ko‘rinadi).
#   2. get_main_keyboard() funksiyasini yarating — tugmalar ro‘yxatini qaytarsin.
#   3. handlers.py da foydalanuvchiga javob yuborayotganda:
#      await message.answer("Matn", reply_markup=get_main_keyboard())
#   4. resize_keyboard=True — tugmalar ekranga moslashadi (kichik ekranda ham).
#
# =============================================================================

# Quyidagi kod namuna. Ishlatish uchun commentlarni olib tashlang va
# handlers.py da reply_markup=get_main_keyboard() qo‘shing.

# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#
# def get_main_keyboard():
#     """Asosiy menyu: bitta qatorda «Namuna matn» tugmasi."""
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="Namuna matn")],
#             # Yangi qator: [KeyboardButton(text="Yordam")],
#         ],
#         resize_keyboard=True,  # Tugmalar ekran o‘lchamiga moslashadi
#     )
