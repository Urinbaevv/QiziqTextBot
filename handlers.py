# =============================================================================
# handlers.py — Xabarlarni qayta ishlash va matnni 50 shriftda ko‘rsatish
# =============================================================================
#
# Bu faylda uchta asosiy narsa bor:
#   1. Shrift jadvallari — har bir «chiroyli» shrift uchun A→𝐀, B→𝐁 kabi
#      almashtirish lug‘ati. Unicode da bunday belgilar alohida bloklarda.
#   2. Matnni 50 shriftda formatlash — foydalanuvchi yozgan matnni har bir
#      jadval orqali o‘tkazib, 50 qator qilib chiqarish.
#   3. Handlerlar — /start buyrug‘i va oddiy matn xabarlariga javob berish.
#
# =============================================================================

from aiogram import Router, F
# Router — xabarlarni «qaysi funksiyaga yuborish»ni hal qiladi (marshrutizator).
# F — filter: F.text = «xabarda matn bor», Command("start") = «/start buyrug‘i».

from aiogram.types import Message
# Message — foydalanuvchi yuborgan xabar ob’ekti. message.text = matn, message.answer() = javob.

from aiogram.filters import Command
# Command — buyruqlarni aniqlash uchun. Masalan: Command("start") = /start bosilganda.


# Router yaratamiz. Barcha handler funksiyalarimiz (cmd_start, handle_text) shu
# router ga bog‘lanadi. bot.py da dp.include_router(router) qilib ulaymiz.
router = Router()


# -----------------------------------------------------------------------------
# Shrift jadvali yaratish
# -----------------------------------------------------------------------------
# Unicode da oddiy A, B, C emas, balki 𝐀, 𝐁, 𝐂 (qalin) yoki 𝐴, 𝐵, 𝐶 (kursiv)
# kabi belgilar mavjud. Har bir shrift uchun «oddiy belgi → chiroyli belgi»
# lug‘ati kerak. _make_font_table shu lug‘atni avtomatik yaratadi.
# Parametrlar — Unicode dagi boshlang‘ich kod (hex): A harfi qaysi kodda,
# a harfi qaysi kodda, 0 raqami qaysi kodda. None = o‘sha turdagi belgilarni
# o‘zgartirmaymiz (masalan, kursivda raqamlar ko‘p mavjud emas).
# -----------------------------------------------------------------------------
def _make_font_table(upper_base: int, lower_base: int, digit_base: int | None):
    """
    Bitta Unicode-shrift uchun belgilar almashtirish jadvalini (lug‘at) yaratadi.
    upper_base — A harfining Unicode kodi (bosh harflar A–Z shu koddan ketma-ket).
    lower_base — a harfining Unicode kodi (kichik harflar a–z).
    digit_base — 0 raqamining Unicode kodi (0–9). None bo‘lsa raqamlarni
                 jadvalga kiritmaymiz, matnda 0–9 o‘zgarishsiz qoladi.
    Qaytardi: dict — kalit = oddiy belgi (str), qiymat = chiroyli belgi (str).
    """
    table = {}

    # A–Z: 26 ta bosh harf. ASCII da A=65, B=66, ... Z=90.
    # chr(65 + i) — 65, 66, ... 90 kodli belgilar (A, B, ..., Z).
    # chr(upper_base + i) — shu shriftdagi A, B, ..., Z (masalan qalin: 𝐀, 𝐁, ...).
    for i in range(26):
        table[chr(65 + i)] = chr(upper_base + i)
        table[chr(97 + i)] = chr(lower_base + i)  # a=97, b=98, ... z=122

    # 0–9 raqamlari. digit_base None bo‘lmasa, 0, 1, ..., 9 ni ham jadvalga
    # qo‘shamiz. ASCII: 0=48, 1=49, ... 9=57.
    if digit_base is not None:
        for i in range(10):
            table[chr(48 + i)] = chr(digit_base + i)

    return table


# -----------------------------------------------------------------------------
# 50 ta shrift ro‘yxati
# -----------------------------------------------------------------------------
# Har bir element: (shrift_nomi, almashtirish_jadvali). Nom foydalanuvchiga
# ko‘rinadi (Bold: ..., Italic: ...). Kodlar (0x1D400 va h.k.) Unicode standartidan:
# Mathematical Alphanumeric Symbols (U+1D400–...) va Enclosed Alphanumerics va boshqalar.
# 0x — o‘n oltilik son (hex). Python da chr(0x1D400) = 𝐀 (qalin A).
# -----------------------------------------------------------------------------
FONTS = [
    ("Bold", _make_font_table(0x1D400, 0x1D41A, 0x1D7CE)),
    ("Italic", _make_font_table(0x1D434, 0x1D44E, None)),
    ("Bold Italic", _make_font_table(0x1D468, 0x1D482, None)),
    ("Script", _make_font_table(0x1D49C, 0x1D4B6, None)),
    ("Bold Script", _make_font_table(0x1D4D0, 0x1D4EA, None)),
    ("Fraktur (Gothic)", _make_font_table(0x1D504, 0x1D51E, None)),
    ("Bold Fraktur", _make_font_table(0x1D56C, 0x1D586, None)),
    ("Double-struck", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Sans-serif", _make_font_table(0x1D5A0, 0x1D5BA, 0x1D7E2)),
    ("Sans Bold", _make_font_table(0x1D5D4, 0x1D5EE, 0x1D7EC)),
    ("Sans Italic", _make_font_table(0x1D608, 0x1D622, 0x1D7F6)),
    ("Sans Bold Italic", _make_font_table(0x1D63C, 0x1D656, 0x1D800)),
    ("Monospace", _make_font_table(0x1D670, 0x1D68A, 0x1D7FA)),
    ("Fullwidth", _make_font_table(0xFF21, 0xFF41, 0xFF10)),
    ("Circled", _make_font_table(0x24B6, 0x24D0, None)),
    ("Parenthesized", _make_font_table(0x1F110, 0x249C, None)),
    ("Negative Circled", _make_font_table(0x1F130, 0x1F150, None)),
    ("Cursive", _make_font_table(0x1D49C, 0x1D4B6, None)),
    ("Blackboard", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Typewriter", _make_font_table(0x1D670, 0x1D68A, 0x1D7FA)),
    ("Bubble", _make_font_table(0x24B6, 0x24D0, None)),
    ("Serif Bold", _make_font_table(0x1D400, 0x1D41A, 0x1D7CE)),
    ("Serif Italic", _make_font_table(0x1D434, 0x1D44E, None)),
    ("Serif Bold Italic", _make_font_table(0x1D468, 0x1D482, None)),
    ("Sans Serif", _make_font_table(0x1D5A0, 0x1D5BA, 0x1D7E2)),
    ("Gothic", _make_font_table(0x1D504, 0x1D51E, None)),
    ("Gothic Bold", _make_font_table(0x1D56C, 0x1D586, None)),
    ("Wide", _make_font_table(0xFF21, 0xFF41, 0xFF10)),
    ("Outlined", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Math Bold", _make_font_table(0x1D400, 0x1D41A, 0x1D7CE)),
    ("Math Italic", _make_font_table(0x1D434, 0x1D44E, None)),
    ("Math Script", _make_font_table(0x1D49C, 0x1D4B6, None)),
    ("Math Fraktur", _make_font_table(0x1D504, 0x1D51E, None)),
    ("Math Double-struck", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Math Sans", _make_font_table(0x1D5A0, 0x1D5BA, 0x1D7E2)),
    ("Math Sans Bold", _make_font_table(0x1D5D4, 0x1D5EE, 0x1D7EC)),
    ("Math Sans Italic", _make_font_table(0x1D608, 0x1D622, 0x1D7F6)),
    ("Math Monospace", _make_font_table(0x1D670, 0x1D68A, 0x1D7FA)),
    ("Enclosed Circled", _make_font_table(0x24B6, 0x24D0, None)),
    ("Enclosed Negative", _make_font_table(0x1F130, 0x1F150, None)),
    ("Enclosed Parenthesized", _make_font_table(0x1F110, 0x249C, None)),
    ("Style Bold", _make_font_table(0x1D400, 0x1D41A, 0x1D7CE)),
    ("Style Italic", _make_font_table(0x1D434, 0x1D44E, None)),
    ("Style Script", _make_font_table(0x1D49C, 0x1D4B6, None)),
    ("Style Fraktur", _make_font_table(0x1D504, 0x1D51E, None)),
    ("Style Double-struck", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Style Sans", _make_font_table(0x1D5A0, 0x1D5BA, 0x1D7E2)),
    ("Style Sans Bold", _make_font_table(0x1D5D4, 0x1D5EE, 0x1D7EC)),
    ("Style Sans Italic", _make_font_table(0x1D608, 0x1D622, 0x1D7F6)),
    ("Style Monospace", _make_font_table(0x1D670, 0x1D68A, 0x1D7FA)),
    ("Style Fullwidth", _make_font_table(0xFF21, 0xFF41, 0xFF10)),
    ("Style Circled", _make_font_table(0x24B6, 0x24D0, None)),
    ("Style Negative Circled", _make_font_table(0x1F130, 0x1F150, None)),
    ("Style Parenthesized", _make_font_table(0x1F110, 0x249C, None)),
    ("Style Bold Script", _make_font_table(0x1D4D0, 0x1D4EA, None)),
    ("Style Bold Italic", _make_font_table(0x1D468, 0x1D482, None)),
    ("Style Bold Fraktur", _make_font_table(0x1D56C, 0x1D586, None)),
    ("Style Sans Bold Italic", _make_font_table(0x1D63C, 0x1D656, 0x1D800)),
    ("Style Cursive", _make_font_table(0x1D49C, 0x1D4B6, None)),
    ("Style Blackboard", _make_font_table(0x1D538, 0x1D552, 0x1D7D8)),
    ("Style Typewriter", _make_font_table(0x1D670, 0x1D68A, 0x1D7FA)),
    ("Style Bubble", _make_font_table(0x24B6, 0x24D0, None)),
]

# Ro‘yxatda 50 tadan ortiq bo‘lmasligini ta'minlaymiz. [ :50 ] — birinchi 50 ta element.
FONTS = FONTS[:50]


# -----------------------------------------------------------------------------
# Bitta shriftni matnga qo‘llash
# -----------------------------------------------------------------------------
# table.get(c, c): agar c jadvalda bo‘lsa (A, a, 0, ...), almashtirilgan belgi
# qaytadi; bo‘lmasa (probelsiz, tinish, kirillitsa) c o‘zi qaytadi. Shuning uchun
# «Hello 123» kabi matnda faqat lotin va raqam o‘zgaradi, qolgani qoladi.
# -----------------------------------------------------------------------------
def apply_font(text: str, table: dict) -> str:
    """
    Matnga bitta shrift jadvalini qo‘llaydi: har bir belgi uchun jadvalda
    almashtirish bormi tekshiradi, bor bo‘lsa almashtiradi, yo‘q bo‘lsa o‘zgartirmaydi.
    """
    return "".join(table.get(c, c) for c in text)


# -----------------------------------------------------------------------------
# Matnni barcha 50 shriftda formatlash
# -----------------------------------------------------------------------------
# Har bir shrift uchun apply_font chaqilib, faqat formatlangan matn qatorlar
# ro‘yxati qaytariladi (shrift nomi chiqarilmaydi). Har bir qator alohida
# <code>...</code> ichida — ustiga bosganda nusxalanadi.
# -----------------------------------------------------------------------------
def format_text_in_all_fonts(text: str) -> list[str]:
    """
    Matnni barcha 50 shriftda formatlaydi.
    Qaytardi: qatorlar ro‘yxati — har biri faqat chiroyli matn (shrift nomisiz).
    """
    lines = []
    for name, table in FONTS:
        styled = apply_font(text, table)
        lines.append(styled)
    return lines


def _escape_html(text: str) -> str:
    """HTML da maxsus belgilarni escape qiladi, xabar buzilmasin."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# =============================================================================
# Handlerlar — qaysi xabar kelganda qanday javob berish
# =============================================================================
# @router.message(...) — dekorator: «shu turdagi xabar kelganda quyidagi
# funksiyani chaqir». Command("start") — faqat /start buyrug‘i. F.text — matn
# bor har qanday xabar (lekin buyruq emas). Handlerlar tartibda tekshiriladi:
# birinchi /start, keyin matn. Shuning uchun /start yuborilsa, cmd_start
# chaqiladi, handle_text emas (ya'ni /start 50 shriftda chiqarilmaydi).
# =============================================================================


# /start buyrug‘i — salomlashish va bot haqida qisqa ma'lumot
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Foydalanuvchi /start tugmasini bosganda yoki /start yozganda chaqiladi.
    Javob: salomlashish matni va botdan qanday foydalanish, nima uchun kerak.
    """
    welcome = (
        "Salom! 👋\n\n"
        "Men **Chiroyli matn** botiman. Istalgan matningizni (ism, laqab, ibora) "
        "50 xil Unicode-shriftda ko‘rsataman. Shriftlarni nusxalab Telegram profil ismi, "
        "bio yoki chatlarda ishlatishingiz mumkin.\n\n"
        "**Qanday ishlatish:**\n"
        "Istalgan matn yozing — men uni 50 qatorda, har biri alohida shriftda chiqaraman. "
        "Kerakli qator ustiga bosing — u nusxalanadi (copy).\n\n"
        "Qisqa matn yozing (Telegram xabar 4096 belgi bilan chegaralangan)."
    )
    # parse_mode="Markdown" — **matn** qalin, \n yangi qator sifatida ko‘rsatiladi.
    await message.answer(welcome, parse_mode="Markdown")


# Istalgan matnli xabar (buyruq emas)
@router.message(F.text)
async def handle_text(message: Message):
    """
    Foydalanuvchi /start dan boshqa matn yozganda (masalan "Salom" yoki "Ali")
    chaqiladi. Matnni 50 shriftda formatlab, code blok ichida yuboradi.
    """
    # strip() — bosh va oxiridagi bo‘shliqlarni olib tashlaydi.
    user_text = message.text.strip()

    # Agar faqat probel yuborilsa, user_text bo‘sh bo‘ladi. Bu holda
    # formatlash mantiqsiz — yo‘riqnoma yuboramiz.
    if not user_text:
        await message.answer(
            "Istalgan matn yozing (masalan, ismingiz), men uni 50 xil shriftda ko‘rsataman."
        )
        return

    # Matnni 50 qatorga (har biri shrift nomi + formatlangan matn) aylantiramiz.
    lines = format_text_in_all_fonts(user_text)

    # Har bir qatorni alohida <code>...</code> ichiga olamiz — Telegram da
    # qator ustiga bosganda faqat shu qator tanlanadi va nusxalash oson bo‘ladi.
    # HTML da &, <, > escape qilish kerak, aks holda xabar buziladi.
    code_lines = [f"<code>{_escape_html(line)}</code>" for line in lines]
    html_message = "\n".join(code_lines)

    # Telegram bitta xabarda maksimum 4096 belgi. Agar ortiq bo‘lsa, qirqamiz.
    if len(html_message) > 4096:
        # Qatorlarni kamaytirib, oxiriga eslatma qo‘shamiz.
        part = []
        n = 0
        for line in code_lines:
            if n + len(line) + 1 <= 4080:
                part.append(line)
                n += len(line) + 1
            else:
                break
        part.append("<code>⚠ Qirqib tashlandi (4096 belgi). Qisqaroq yozing.</code>")
        html_message = "\n".join(part)

    await message.answer(html_message, parse_mode="HTML")
