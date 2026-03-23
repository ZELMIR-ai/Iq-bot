import asyncio
import random
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# ==============================
# НАСТРОЙКИ
# ==============================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_СЮДА")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ==============================
# СОСТОЯНИЯ
# ==============================
class IQTest(StatesGroup):
    question = State()
    captcha = State()
    analyzing = State()

# ==============================
# ВОПРОСЫ
# ==============================
QUESTIONS = [
    {
        "text": "❓ Вопрос 1 из 15\n\n🧠 Если в комнате 3 яблока и ты забрал 2 — сколько у ТЕБЯ яблок?",
        "options": ["1", "2", "3", "Я не ем яблоки"],
        "correct": "2"
    },
    {
        "text": "❓ Вопрос 2 из 15\n\n🐄 Сколько месяцев в году имеют 28 дней?",
        "options": ["Только февраль", "Один", "Все 12", "Зависит от года"],
        "correct": "Все 12"
    },
    {
        "text": "❓ Вопрос 3 из 15\n\n📐 Если квадрат имеет сторону 5 см, чему равна его площадь?",
        "options": ["10 см²", "20 см²", "25 см²", "15 см²"],
        "correct": "25 см²"
    },
    {
        "text": "❓ Вопрос 4 из 15\n\n🚀 Может ли мужчина жениться на сестре своей вдовы?",
        "options": ["Нет, это незаконно", "Да, если попросит", "Нет, он же мёртв", "Только в Европе"],
        "correct": "Нет, он же мёртв"
    },
    {
        "text": "❓ Вопрос 5 из 15\n\n🌍 Столица Австралии — это...",
        "options": ["Сидней", "Мельбурн", "Канберра", "Брисбен"],
        "correct": "Канберра"
    },
    {
        "text": "❓ Вопрос 6 из 15\n\n🔥 Что станет с красной шапочкой, если её стирать при 90°C?",
        "options": ["Сядет", "Выцветет", "Ничего", "Это персонаж, у неё нет шапки"],
        "correct": "Ничего"
    },
    {
        "text": "❓ Вопрос 7 из 15\n\n🧮 Чему равно: 2 + 2 × 2?",
        "options": ["8", "6", "4", "16"],
        "correct": "6"
    },
    {
        "text": "❓ Вопрос 8 из 15\n\n🐟 Сколько животных Моисей взял на ковчег каждого вида?",
        "options": ["2", "7", "По одному", "Это был Ной, а не Моисей"],
        "correct": "Это был Ной, а не Моисей"
    },
    {
        "text": "❓ Вопрос 9 из 15\n\n⚡ Что тяжелее: килограмм железа или килограмм ваты?",
        "options": ["Железо", "Вата", "Одинаково", "Зависит от влажности"],
        "correct": "Одинаково"
    },
    {
        "text": "❓ Вопрос 10 из 15\n\n🌙 Некоторые месяцы имеют 31 день. Сколько месяцев имеют 30 дней?",
        "options": ["4", "6", "11", "Все кроме февраля"],
        "correct": "11"
    },
    {
        "text": "❓ Вопрос 11 из 15\n\n🔢 В какой стране придумали арабские цифры?",
        "options": ["Аравия", "Египет", "Индия", "Иран"],
        "correct": "Индия"
    },
    {
        "text": "❓ Вопрос 12 из 15\n\n🛌 Доктор даёт тебе 3 таблетки и говорит принимать каждые полчаса. Через сколько времени кончатся таблетки?",
        "options": ["1,5 часа", "1 час", "30 минут", "Час"],
        "correct": "1 час"
    },
    {
        "text": "❓ Вопрос 13 из 15\n\n🌿 Что происходит с растением если его не поливать 3 месяца?",
        "options": ["Ничего", "Засохнет", "Уснёт", "Зависит от растения"],
        "correct": "Зависит от растения"
    },
    {
        "text": "❓ Вопрос 14 из 15\n\n🐓 Если петух снесёт яйцо на самой верхушке крыши — в какую сторону оно скатится?",
        "options": ["На юг", "По ветру", "Петух не несёт яйца", "Упадёт вертикально"],
        "correct": "Петух не несёт яйца"
    },
    {
        "text": "❓ Вопрос 15 из 15\n\n🧠 Последний вопрос!\n\nЧему равно: 0,5 + 0,5 × 0?",
        "options": ["0", "0,5", "1", "Не существует"],
        "correct": "0,5"
    },
]

CAPTCHA = {
    "text": (
        "🔐 Вопрос 15.5 из 15 — КАПЧА\n\n"
        "Для подтверждения личности введи ПРАВИЛЬНЫЙ ответ:\n\n"
        "На картинке написано: «Выбери ВСЕ светофоры»\n\n"
        "🚦🚗🚦🌳🚦🏠🚦🐈\n\n"
        "Какой из вариантов ты выбираешь?"
    ),
    "options": [
        "Все светофоры 🚦",
        "Только зелёные 🟢",
        "Все картинки 🖼",
        "Пропустить капчу"
    ]
}

ANALYSIS_COMMENTS = [
    (30, 39, "💀 КРИТИЧЕСКИЙ УРОВЕНЬ",
     "Такой результат встречается лишь у 0.1% населения планеты.\n"
     "Учёные считают это научным феноменом.\n"
     "Твой мозг умудрился набрать балл ниже, чем рандомное угадывание.\n\n"
     "Но знаешь что? Ты лучше пользователя <b>Даниил Коротких</b>. "
     "Это единственная хорошая новость на сегодня. 🫡"),

    (40, 49, "😬 ОЧЕНЬ НИЗКИЙ УРОВЕНЬ",
     "Поздравляем! Ты побил рекорд нашей системы за последние 3 года.\n"
     "Большинство лабораторных мышей показывают результат лучше.\n\n"
     "Но есть и хорошая новость: ты всё ещё умнее пользователя "
     "<b>Даниил Коротких</b>. Это что-то значит... наверное. 🐭"),

    (50, 59, "😐 НИЗКИЙ УРОВЕНЬ",
     "Ну... хотя бы ты знаешь как пользоваться Telegram, это уже что-то.\n"
     "Рекомендуем больше читать книги, смотреть Discovery и, возможно, "
     "не есть перед важными тестами.\n\n"
     "P.S. Даниил Коротких сделал бы хуже. Утешься этим фактом. 📚"),

    (60, 70, "😅 НЕМНОГО ВЫШЕ ДНА",
     "Нейросеть проанализировала твои ответы и пришла к выводу:\n"
     "ты иногда думаешь, но редко доводишь мысль до конца.\n"
     "Есть потенциал, но он глубоко скрыт.\n\n"
     "Главное — ты умнее <b>Даниил Коротких</b>. "
     "А это, поверь, не так просто. 🎖"),
]

def get_analysis(iq: int):
    for lo, hi, title, text in ANALYSIS_COMMENTS:
        if lo <= iq <= hi:
            return title, text
    return "💀 ОШИБКА ИЗМЕРЕНИЯ", "Результат настолько низкий, что прибор сломался."

def make_keyboard(options):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i, opt in enumerate(options):
        row.append(opt)
        if len(row) == 2:
            keyboard.add(*row)
            row = []
    if row:
        keyboard.add(*row)
    return keyboard

# ==============================
# /start
# ==============================
@dp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🚀 Начать тест!")
    await message.answer(
        "🧠 <b>IQ ТЕСТ — ОФИЦИАЛЬНАЯ ПРОВЕРКА ИНТЕЛЛЕКТА</b>\n\n"
        "Добро пожаловать в сертифицированный тест IQ!\n\n"
        "📋 Тебя ждут:\n"
        "• 15 вопросов на логику и эрудицию\n"
        "• 1 капча для подтверждения личности\n"
        "• Точный анализ твоего интеллекта\n\n"
        "⏱ Среднее время прохождения: 5-7 минут\n\n"
        "Готов? Нажми кнопку ниже 👇",
        reply_markup=keyboard
    )

@dp.message_handler(lambda m: m.text == "🚀 Начать тест!", state="*")
async def start_test(message: types.Message, state: FSMContext):
    await state.finish()
    await IQTest.question.set()
    await state.update_data(q_index=0, correct=0)
    await send_question(message, state)

async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("q_index", 0)

    if q_index >= len(QUESTIONS):
        await IQTest.captcha.set()
        await send_captcha(message, state)
        return

    q = QUESTIONS[q_index]
    await message.answer(q["text"], reply_markup=make_keyboard(q["options"]))

@dp.message_handler(state=IQTest.question)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("q_index", 0)
    correct_count = data.get("correct", 0)

    if q_index < len(QUESTIONS):
        q = QUESTIONS[q_index]
        if message.text not in q["options"]:
            await message.answer("⚠️ Пожалуйста, выбери один из вариантов кнопками!")
            return
        if message.text == q["correct"]:
            correct_count += 1

    await state.update_data(q_index=q_index + 1, correct=correct_count)
    await send_question(message, state)

async def send_captcha(message: types.Message, state: FSMContext):
    await message.answer(CAPTCHA["text"], reply_markup=make_keyboard(CAPTCHA["options"]))

@dp.message_handler(state=IQTest.captcha)
async def handle_captcha(message: types.Message, state: FSMContext):
    if message.text not in CAPTCHA["options"]:
        await message.answer("⚠️ Выбери один из вариантов!")
        return

    await IQTest.analyzing.set()
    await message.answer(
        "✅ Капча пройдена! Начинаю анализ результатов...",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await run_analysis(message, state)

async def run_analysis(message: types.Message, state: FSMContext):
    frames = [
        "🔬 Анализирую нейронные связи........",
        "📊 Обрабатываю данные теста..........",
        "🧬 Сканирую мозговую активность.....",
        "💡 Вычисляю коэффициент интеллекта..",
        "🖥 Запускаю финальный алгоритм.......",
        "📡 Синхронизация с базой данных.....",
        "⚗️ Анализ завершается..................",
    ]

    sent = await message.answer(frames[0])
    for frame in frames[1:]:
        await asyncio.sleep(1.2)
        await sent.edit_text(frame)

    await asyncio.sleep(1.5)

    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓░░░░░░░░░  10%")
    await asyncio.sleep(0.8)
    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓▓▓░░░░░░░  30%")
    await asyncio.sleep(0.8)
    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓░░░░░  50%")
    await asyncio.sleep(0.8)
    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓░░░  70%")
    await asyncio.sleep(0.8)
    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓▓▓░  90%")
    await asyncio.sleep(1)
    await sent.edit_text("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓▓▓▓  100%\n\n✅ Анализ завершён!")
    await asyncio.sleep(1.5)

    iq = random.randint(30, 70)
    title, comment = get_analysis(iq)

    await message.answer(
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>РЕЗУЛЬТАТ IQ ТЕСТА</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 Твой IQ: <b>{iq}</b>\n\n"
        f"Уровень: {title}\n\n"
        f"📝 <b>Вердикт нейросети:</b>\n\n"
        f"{comment}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>© Certified IQ Test 2025. Все результаты точны на 146%</i>"
    )

    await asyncio.sleep(1)
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        photo = types.InputFile(os.path.join(BASE_DIR, "losash.png"))
        await message.answer_photo(
            photo=photo,
            caption=(
                "😢 <b>Лосяш тоже расстроен твоим результатом...</b>\n\n"
                "Но не переживай! Ты всё равно лучше, чем Даниил Коротких 🫡\n\n"
                "🔄 Хочешь попробовать ещё раз? /start"
            )
        )
    except Exception:
        await message.answer(
            "😢 <b>Лосяш плачет из-за твоего результата...</b>\n\n"
            "🔄 Попробовать снова: /start"
        )

    await state.finish()

# ==============================
# /help
# ==============================
@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>IQ Тест — Справка</b>\n\n"
        "Это официальный тест для проверки коэффициента интеллекта.\n\n"
        "Команды:\n"
        "/start — начать тест\n"
        "/help — эта справка\n\n"
        "<i>Тест абсолютно честный и научно обоснованный™</i>"
    )

# ==============================
# Запуск
# ==============================
if __name__ == "__main__":
    print("🤖 IQ Prank Bot запущен!")
    executor.start_polling(dp, skip_updates=True)
