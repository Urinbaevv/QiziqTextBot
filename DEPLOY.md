# Railway da botni deploy qilish (o‘quv qo‘llanma)

Bu qo‘llanma talabalar uchun **Beautiful Text Bot** ni **Railway** platformasida bepul deploy qilish bo‘yicha qadam-baqadam ko‘rsatma.

---

## Nima uchun Railway?

- **Bepul** rejada loyiha deploy qilish mumkin (oyiga ma’lum kredit).
- GitHub repositoriyani ulab, har safar `git push` qilganda avtomatik yangilanadi.
- Token va maxfiy ma’lumotlarni **Variables** da xavfsiz saqlash.
- Bot 24/7 ishlaydi (kompyuteringiz yopiq bo‘lsa ham).

---

## Oldingi shartlar

1. **GitHub** hisobingiz va loyiha GitHub da bo‘lishi kerak.
2. **Bot tokeni** — [@BotFather](https://t.me/BotFather) dan olgan `BOT_TOKEN`.
3. Loyiha mahalliy kompyuteringizda ishlayotgan bo‘lishi kerak (`python bot.py`).

---

## 1-qadam: Loyihani GitHub ga yuklash

Agar loyiha hali GitHub da bo‘lmasa:

```bash
cd BeautifulTextBot
git init
git add .
git commit -m "Railway deploy uchun tayyor"
```

GitHub da yangi repository yarating (masalan: `BeautifulTextBot`). Keyin:

```bash
git remote add origin https://github.com/FAMILYANGIZINGIZ/BeautifulTextBot.git
git branch -M main
git push -u origin main
```

`FAMILYANGIZINGIZ` o‘rniga o‘zingizning GitHub username ingizni yozing. Repository nomi ham o‘zingizniki bo‘lishi mumkin.

---

## 2-qadam: Railway da hisob ochish va loyiha qo‘shish

1. [railway.app](https://railway.app) ga kiring.
2. **Login** → **GitHub** bilan kiring (GitHub hisobingizga ulash tavsiya etiladi).
3. **New Project** (yoki **Start a New Project**) bosing.
4. **Deploy from GitHub repo** tanlang.
5. GitHub dan **BeautifulTextBot** (yoki siz yaratgan repo) ni tanlang.
6. Agar repo ko‘rinmasa — **Configure GitHub App** orqali kerakli repolariga ruxsat bering.

Shundan keyin Railway repo ni klon qiladi va **build** boshlaydi.

---

## 3-qadam: BOT_TOKEN ni o‘rnatish

Bot ishlashi uchun token **maxfiy** bo‘lishi kerak va kodda emas, balki **muhit o‘zgaruvchisi** sifatida beriladi.

1. Railway da ochilgan loyihangizda **BeautifulTextBot** servisiga bosing.
2. **Variables** yoki **Settings** → **Variables** bo‘limiga o‘ting.
3. **New Variable** / **Add Variable** bosing.
4. Nom: `BOT_TOKEN`, qiymat: BotFather dan olgan token (masalan: `8551015577:AAGcReowfc6bMHb0HG4WTxGmG-8oorAS-hk`).
5. **Add** yoki **Save** bosing.

**Muhim:** Token ni hech kimga yubormang va GitHub ga commit qilmang. `.env` fayli `.gitignore` da bo‘lgani uchun u repoga kirmaydi.

---

## 4-qadam: Start Command tekshirish (kerak bo‘lsa)

Railway odatda `nixpacks.toml` yoki `Procfile` dan start buyrug‘ini oladi. Loyihada allaqachon quyidagilar bor:

- **nixpacks.toml** — `commands = ["python bot.py"]`
- **Procfile** — `worker: python bot.py`

Agar build muvaffaqiyatli, lekin bot ishlamasa:

1. **Settings** → **Deploy** (yoki **Service Settings**).
2. **Start Command** maydonini toping.
3. Agar bo‘sh bo‘lsa, qo‘ying: `python bot.py`.
4. **Deploy** ni qayta ishga tushiring (Redeploy).

---

## 5-qadam: Deploy va loglar

1. **Deployments** bo‘limida oxirgi deploy ni ko‘ring. **Building** → **Success** bo‘lishi kerak.
2. **View Logs** bosing — konsolda bot ishga tushganida `INFO` xabarlari ko‘rinadi.
3. Telegram da botga xabar yuborib tekshiring: `/start` va keyin istalgan matn.

Agar xato bo‘lsa, loglarda ko‘pincha:

- `BOT_TOKEN topilmadi` — Variables da `BOT_TOKEN` qo‘yilmagan yoki nomi noto‘g‘ri.
- `No start command` — Start Command ni `python bot.py` qilib o‘rnating.

---

## Loyihadagi Railway bilan bog‘liq fayllar

| Fayl            | Vazifasi |
|-----------------|----------|
| **Procfile**    | `worker: python bot.py` — worker tipidagi process (veb-server emas). |
| **nixpacks.toml** | Build va start buyrug‘ini Nixpacks ga beradi; `python bot.py` ishga tushadi. |
| **runtime.txt** | Python versiyasi (3.11.9); Railway bu versiyani ishlatadi. |
| **.gitignore** | `.env` va `venv` ni repoga kiritmaydi (token xavfsizligi). |

---

## Tez-tez beriladigan savollar

**Bot javob bermayapti.**  
→ Loglarni tekshiring. Token to‘g‘ri va Start Command `python bot.py` ekanligini tekshiring.

**Build xato bermoqda.**  
→ `requirements.txt` da paketlar to‘g‘ri (aiogram, python-dotenv). Python 3.11 ishlatilayotganini tekshiring.

**Tokenni qayerda saqlayman?**  
→ Faqat Railway **Variables** da. Kodda va GitHub da saqlamang.

**Bepul rejada limit bormi?**  
→ Railway bepul kredit beradi; oddiy bot uchun oyiga yetarli bo‘ladi. Limit **Usage** bo‘limida ko‘rinadi.

---

Muvaffaqiyatli deploy qilganingizdan keyin bot 24/7 ishlaydi va har safar `git push` qilganda Railway avtomatik yangi versiyani deploy qiladi.
