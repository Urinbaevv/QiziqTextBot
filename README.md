## Bu bot nima va nima uchun kerak

**Beautiful Text Bot** — bu Telegram-bot quyidagilarni qiladi:

1. **Foydalanuvchidan istalgan matnni qabul qiladi** (masalan, ism yoki qisqa ibora).
2. **Ushbu matnni 50 xil Unicode-shriftga aylantiradi** — qalin, kursiv, gotik, «pufakchalar», monospace va boshqalar.
3. **Natijani bitta xabar bilan yuboradi** — har bir qator matnning bitta uslubdagi variantidir.

Bunday matnni nusxalab, masalan, **Telegram profilidagi to‘liq ism** (Full Name), imzoda yoki chatlarda ajralib turish uchun ishlatish mumkin.

Bot **mumkin qadar oddiy** yozilgan — aiogram 3.24 da bot qanday ishlashi, matn qayerdan kelishi, «chiroyli» shrift qanday qo‘llanishi va hammasi qanday bitta javobga yig‘ilishi bo‘yicha o‘rganish uchun.

---

## Loyiha tuzilishi

Loyiha **majburiy** fayllardan iborat:

```
BeautifulTextBot/
├── bot.py          # Kirish nuqtasi: botni ishga tushirish
├── config.py       # Sozlamalarni yuklash (token .env dan)
├── handlers.py     # Xabarlarni qayta ishlash va 50 shrift
├── keyboards.py    # Klaviaturalar (hozircha bo‘sh, kengaytirish uchun)
├── .env            # Bot tokeni (internetga chiqarmang!)
├── requirements.txt
└── README.md      # Ushbu o‘quv maqola
```

Har bir fayl **bitta aniq vazifaga** ega — kodni o‘qish va o‘zgartirish osonroq bo‘ladi.

---

## aiogram 3.24 qanday ishlaydi (qisqacha)

**aiogram** — Telegram uchun Python da botlar yozish kutubxonasi. **3.x** versiyasi **asinxron** koddan (`async` / `await`) foydalanadi.

Asosiy tushunchalar:

- **Bot** — bot ob’ekti, orqali Telegram ga xabarlar yuboriladi.
- **Dispatcher (dp)** — «dispetcher»: yangilanishlarni (xabarlar, tugma bosish va h.k.) qabul qiladi va qaysi qayta ishlovchiga berishni hal qiladi.
- **Router** — «marshrutizator»: unga qayta ishlovchilar bog‘lanadi (masalan: «matnli har qanday xabar uchun `handle_text` funksiyasini chaqir»).
- **Handler** — ma’lum hodisa sodir bo‘lganda chaqiriladigan funksiya (masalan, matn kelganda).

Ishlash zanjiri:

1. Foydalanuvchi botga xabar yozadi.
2. Telegram yangilanishni serverga yuboradi.
3. Bot (long polling orqali) bu yangilanishni oladi.
4. Dispatcher uni Router ga uzatadi.
5. Router mos qayta ishlovchini topadi (filtrlar bo‘yicha, masalan `F.text`).
6. Bizning qayta ishlovchi funksiyamiz chaqiriladi; javobni tuzamiz va `message.answer()` orqali yuboramiz.

Bularning hammasini **klasslarsiz** va murakkab arxitekturasiz — faqat funksiyalar va oddiy ma’lumotlar tuzilmalari bilan qilamiz.

---

## Har bir faylning tahlili

### 1. `config.py` — sozlamalar

**Mas’uliyat:** muhitdan (`.env` faylidan) sozlamalarni yuklash, **bot tokeni kodda saqlanmasin**.

- `load_dotenv()` — `.env` faylini o‘qiydi va o‘zgaruvchilarni `os.environ` ga qo‘yadi.
- `BOT_TOKEN = os.getenv("BOT_TOKEN", "")` — `BOT_TOKEN` o‘zgaruvchisini oladi; bo‘lmasa, bo‘sh qator bo‘ladi.
- `get_token()` — tokenni qaytaradi va bo‘sh emasligini tekshiradi. Bo‘sh bo‘lsa — bot ishga tushmasin, shuning uchun xato chiqaramiz.

Shu bilan qoidaga amal qilamiz: **sirlar (token) — .env da, kod — sirsiz.**

---

### 2. `handlers.py` — xabarlarni qayta ishlash va shriftlar

**Mas’uliyat:** foydalanuvchi matnini qabul qilish, uni 50 Unicode-shriftda bezash va javob yuborish.

#### Router va qayta ishlovchi

- `router = Router()` — barcha xabar qayta ishlovchilar uchun bitta router yaratamiz.
- `@router.message(F.text)` — «matni bor har qanday xabar uchun keyingi funksiyani chaqir».
- `async def handle_text(message: Message)` — bizning funksiyamiz. U **asinchron**, chunki aiogram 3 async da ishlaydi. `message.text` da foydalanuvchi yozgan matn turadi.

#### «Shriftlar» qanday tuzilgan

Unicode da A–Z, a–z va 0–9 ga **o‘xshash** ko‘rinadigan, lekin boshqa yozuvdagi (qalin, kursiv, gotik, doira ichida va h.k.) belgilar bloklari mavjud. Biz rasm chizmaymiz — har bir belgini kerakli blokdagi mos belgiga **almashtiramiz**.

- **Almashtirish jadvali** — lug‘at: oddiy harf → «chiroyli» harf. Masalan: `{'A': '𝐀', 'B': '𝐁', ...}` (qalin shrift).
- `_make_font_table(upper_base, lower_base, digit_base)` funksiyasi bunday jadvalni **yaratadi**:
  - A–Z uchun `upper_base` dan boshlanadigan Unicode kodlari;
  - a–z uchun — `lower_base` dan;
  - 0–9 uchun — `digit_base` dan (`None` berilsa, raqamlarni o‘zgartirmaymiz).
- `FONTS` ro‘yxati — 50 juftlik: (shrift nomi, almashtirish jadvali). Nomlar tushunariligi uchun (xabarda chiqarmaymiz, lekin xohlasak har qatorni imzolash mumkin).

#### Formatlash qanday qo‘llanadi

- `apply_font(text, table)` — `text` ning har bir belgisidan o‘tadi; agar `table` da almashtirish bo‘lsa, uni qo‘yadi, aks holda belgini o‘zgartirmaydi. Shunday qilib nafaqat lotin, balki bo‘shliq, tinish belgilari, kirillitsa ham qoladi (o‘zgarishsiz).
- `format_text_in_all_fonts(text)` — 50 ta jadvalning har biri uchun `apply_font` ni chaqiradi, natijalarni qatorlar ro‘yxatiga yig‘adi va `"\n"` bilan birlashtiradi. Natijada bitta katta xabar: 50 qator, har biri — o‘sha matn o‘z shriftida.

#### Telegram chegarasi

Bitta xabarda **4096 belgidan** ortiq yuborish mumkin emas. Natija uzunroq bo‘lsa, qirqib, «Qisqaroq yozing» degan eslatma qo‘shamiz.

Natijada `handle_text` da: matnni olamiz → 50 shriftda formatlaymiz → kerak bo‘lsa qirqamiz → bitta xabar bilan yuboramiz.

---

### 3. `keyboards.py` — klaviaturalar

**Mas’uliyat:** bu loyihada klaviaturalar ishlatilmaydi — foydalanuvchi oddiygina matn yozadi. Fayl talab qilingan tuzilishga moslash uchun **bo‘sh (izohlar bilan)** qoldirilgan. Keyinroq shu yerga, masalan, «Yordam» yoki «Namuna» tugmasini qo‘shish mumkin.

---

### 4. `bot.py` — kirish nuqtasi

**Mas’uliyat:** botni ishga tushirish.

- `get_token()` — tokenni `config` dan olamiz.
- `Bot(token=token)` — bot ob’ektini yaratamiz.
- `Dispatcher()` — dispetcherni yaratamiz.
- `dp.include_router(router)` — `handlers.py` dagi routerni ulaymiz; unda ro‘yxatdan o‘tgan barcha qayta ishlovchilar ishlay boshlaydi.
- `dp.start_polling(bot)` — Telegram serverlarini so‘rov (long polling) ishga tushiramiz: bot doim «yangi xabarlar bormi?» deb so‘raydi va ularni dispetcherga beradi.

`asyncio.run(main())` orqali ishga tushirish — Pythonda asinxron kodni ishga tushirishning odatiy usuli.

---

### 5. `.env` — token

Faylda bitta qator (tirnoqsiz):

```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

Bot yaratishda [@BotFather](https://t.me/BotFather) beradigan **haqiqiy token** bilan almashtirish kerak. `.env` fayli omborga (repository) kirmasligi kerak (uni `.gitignore` ga qo‘shing).

---

## Botni qanday ishga tushirish

1. Bog‘liqliklarni o‘rnating:
   ```bash
   pip install -r requirements.txt
   ```
2. `.env` da o‘z `BOT_TOKEN` ingizni yozing.
3. Ishga tushiring:
   ```bash
   python bot.py
   ```

Shundan keyin bot har qanday matnli xabarga bitta xabar bilan 50 xil shriftdagi matn variantlari bilan javob beradi.

---

## Birinchi kurs talabasi uchun qisqacha xulosa

- **config.py** — tokenni `.env` dan o‘qiydi.
- **handlers.py** — matnni qayta ishlaydi: 50 ta «shrift» ning har biri uchun harflar va raqamlarni Unicode belgilarga almashtiradi va hammasini bitta xabar bilan yuboradi.
- **keyboards.py** — hozircha ishlatilmaydi.
- **bot.py** — bot va dispetcherni yig‘adi, qayta ishlovchilarni ulaydi va Telegram so‘rovini ishga tushiradi.

Bot mantiqi: **matn oldi → 50 ta almashtirish jadvalini qo‘lladi → natijani bitta xabar bilan yubordi.** Hammasi oddiy funksiyalar va ro‘yxatlar/lug‘atlar orqali, ortiqcha abstraksiyalarsiz.
