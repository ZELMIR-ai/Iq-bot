import telebot
import random
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_ТОКЕН")
bot = telebot.TeleBot(BOT_TOKEN)

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
        "text": "❓ Вопрос 12 из 15\n\n🛌 Доктор даёт тебе 3 таблетки — принимать каждые полчаса. Через сколько кончатся?",
        "options": ["1,5 часа", "1 час", "30 минут", "2 часа"],
        "correct": "1 час"
    },
    {
        "text": "❓ Вопрос 13 из 15\n\n🌿 Что происходит с растением если его не поливать 3 месяца?",
        "options": ["Ничего", "Засохнет", "Уснёт", "Зависит от растения"],
        "correct": "Зависит от растения"
    },
    {
        "text": "❓ Вопрос 14 из 15\n\n🐓 Если петух снесёт яйцо на крыше — в какую сторону оно скатится?",
        "options": ["На юг", "По ветру", "Петух не несёт яйца", "Упадёт вертикально"],
        "correct": "Петух не несёт яйца"
    },
    {
        "text": "❓ Вопрос 15 из 15\n\n🧠 Последний!\n\nЧему равно: 0,5 + 0,5 × 0?",
        "options": ["0", "0,5", "1", "Не существует"],
        "correct": "0,5"
    },
]

CAPTCHA = {
    "text": (
        "🔐 Вопрос 15.5 из 15 — КАПЧА\n\n"
        "На картинке написано: «Выбери ВСЕ светофоры»\n\n"
        "🚦🚗🚦🌳🚦🏠🚦🐈\n\n"
        "Какой вариант выбираешь?"
    ),
    "options": ["Все светофоры 🚦", "Только зелёные 🟢", "Все картинки 🖼", "Пропустить капчу"]
}

ANALYSIS_COMMENTS = [
    (30, 39, "💀 КРИТИЧЕСКИЙ УРОВЕНЬ",
     "Такой результат встречается лишь у 0.1% населения планеты.\n"
     "Учёные считают это научным феноменом.\n\n"
     "Но ты лучше пользователя <b>Даниил Коротких</b>. Это единственная хорошая новость. 🫡"),
    (40, 49, "😬 ОЧЕНЬ НИЗКИЙ УРОВЕНЬ",
     "Большинство лабораторных мышей показывают результат лучше.\n\n"
     "Хорошая новость: ты умнее <b>Даниил Коротких</b>. Это что-то значит... наверное. 🐭"),
    (50, 59, "😐 НИЗКИЙ УРОВЕНЬ",
     "Хотя бы ты знаешь как пользоваться Telegram, это уже что-то.\n\n"
     "P.S. Даниил Коротких сделал бы хуже. Утешься этим фактом. 📚"),
    (60, 70, "😅 НЕМНОГО ВЫШЕ ДНА",
     "Ты иногда думаешь, но редко доводишь мысль до конца.\n\n"
     "Главное — ты умнее <b>Даниил Коротких</b>. А это, поверь, не так просто. 🎖"),
]

def get_analysis(iq):
    for lo, hi, title, text in ANALYSIS_COMMENTS:
        if lo <= iq <= hi:
            return title, text
    return "💀 ОШИБКА ИЗМЕРЕНИЯ", "Результат настолько низкий, что прибор сломался."

def make_keyboard(options):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(options), 2):
        row = options[i:i+2]
        keyboard.add(*[telebot.types.KeyboardButton(o) for o in row])
    return keyboard

user_state = {}

def get_state(uid):
    return user_state.get(uid, {"step": "idle", "q_index": 0, "correct": 0})

def set_state(uid, data):
    user_state[uid] = data

@bot.message_handler(commands=["start"])
def cmd_start(message):
    uid = message.from_user.id
    set_state(uid, {"step": "idle", "q_index": 0, "correct": 0})
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("🚀 Начать тест!"))
    bot.send_message(
        message.chat.id,
        "🧠 <b>IQ ТЕСТ — ОФИЦИАЛЬНАЯ ПРОВЕРКА ИНТЕЛЛЕКТА</b>\n\n"
        "Добро пожаловать в сертифицированный тест IQ!\n\n"
        "📋 Тебя ждут:\n"
        "• 15 вопросов на логику и эрудицию\n"
        "• 1 капча для подтверждения личности\n"
        "• Точный анализ твоего интеллекта\n\n"
        "⏱ Среднее время: 5-7 минут\n\n"
        "Готов? Нажми кнопку ниже 👇",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>IQ Тест — Справка</b>\n\n"
        "/start — начать тест\n"
        "/help — эта справка\n\n"
        "<i>Тест абсолютно честный и научно обоснованный™</i>",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    uid = message.from_user.id
    state = get_state(uid)
    step = state.get("step", "idle")

    if message.text == "🚀 Начать тест!":
        state = {"step": "question", "q_index": 0, "correct": 0}
        set_state(uid, state)
        send_question(message.chat.id, uid)
        return

    if step == "question":
        q_index = state["q_index"]
        correct = state["correct"]
        if q_index < len(QUESTIONS):
            q = QUESTIONS[q_index]
            if message.text not in q["options"]:
                bot.send_message(message.chat.id, "⚠️ Выбери один из вариантов кнопками!")
                return
            if message.text == q["correct"]:
                correct += 1
            state["correct"] = correct
            state["q_index"] = q_index + 1
            set_state(uid, state)
        if state["q_index"] >= len(QUESTIONS):
            state["step"] = "captcha"
            set_state(uid, state)
            bot.send_message(message.chat.id, CAPTCHA["text"], reply_markup=make_keyboard(CAPTCHA["options"]))
        else:
            send_question(message.chat.id, uid)
        return

    if step == "captcha":
        if message.text not in CAPTCHA["options"]:
            bot.send_message(message.chat.id, "⚠️ Выбери один из вариантов!")
            return
        state["step"] = "analyzing"
        set_state(uid, state)
        bot.send_message(
            message.chat.id,
            "✅ Капча пройдена! Начинаю анализ...",
            reply_markup=telebot.types.ReplyKeyboardRemove()
        )
        run_analysis(message.chat.id, uid)
        return

def send_question(chat_id, uid):
    state = get_state(uid)
    q = QUESTIONS[state["q_index"]]
    bot.send_message(chat_id, q["text"], reply_markup=make_keyboard(q["options"]), parse_mode="HTML")

def run_analysis(chat_id, uid):
    frames = [
        "🔬 Анализирую нейронные связи........",
        "📊 Обрабатываю данные теста..........",
        "🧬 Сканирую мозговую активность.....",
        "💡 Вычисляю коэффициент интеллекта..",
        "🖥 Запускаю финальный алгоритм.......",
        "📡 Синхронизация с базой данных.....",
        "⚗️ Анализ завершается..................",
    ]
    msg = bot.send_message(chat_id, frames[0])
    for frame in frames[1:]:
        time.sleep(1.2)
        bot.edit_message_text(frame, chat_id, msg.message_id)

    time.sleep(1.5)

    progress = [
        ("⏳ Финальный подсчёт IQ...\n\n▓░░░░░░░░░  10%", 0.8),
        ("⏳ Финальный подсчёт IQ...\n\n▓▓▓░░░░░░░  30%", 0.8),
        ("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓░░░░░  50%", 0.8),
        ("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓░░░  70%", 0.8),
        ("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓▓▓░  90%", 1.0),
        ("⏳ Финальный подсчёт IQ...\n\n▓▓▓▓▓▓▓▓▓▓  100%\n\n✅ Анализ завершён!", 1.5),
    ]
    for text, delay in progress:
        bot.edit_message_text(text, chat_id, msg.message_id)
        time.sleep(delay)

    iq = random.randint(30, 70)
    title, comment = get_analysis(iq)

    bot.send_message(
        chat_id,
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>РЕЗУЛЬТАТ IQ ТЕСТА</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 Твой IQ: <b>{iq}</b>\n\n"
        f"Уровень: {title}\n\n"
        f"📝 <b>Вердикт нейросети:</b>\n\n"
        f"{comment}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>© Certified IQ Test 2025. Все результаты точны на 146%</i>",
        parse_mode="HTML"
    )

    time.sleep(1)
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(BASE_DIR, "losash.png"), "rb") as photo:
            bot.send_photo(
                chat_id, photo,
                caption=(
                    "😢 <b>Лосяш тоже расстроен твоим результатом...</b>\n\n"
                    "Но не переживай! Ты всё равно лучше, чем Даниил Коротких 🫡\n\n"
                    "🔄 Хочешь ещё раз? /start"
                ),
                parse_mode="HTML"
            )
    except Exception:
        bot.send_message(
            chat_id,
            "😢 <b>Лосяш плачет из-за твоего результата...</b>\n\n🔄 Попробовать снова: /start",
            parse_mode="HTML"
        )

    set_state(uid, {"step": "idle", "q_index": 0, "correct": 0})

if __name__ == "__main__":
    print("🤖 IQ Prank Bot запущен!")
    bot.infinity_polling()
