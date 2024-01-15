import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from dotenv import load_dotenv
from os import getenv
from info import survey, load_data, save_data, result
from time import sleep

# создаём бота
load_dotenv()
token = getenv("BOT_TOKEN")

bot = telebot.TeleBot(token)

# создаём путь к файлу и сохраняем его
data_path = "data.json"
data_users = load_data(data_path)
# создаем нужные клавиатуры
keyboard_1 = InlineKeyboardMarkup()
keyboard_1.row(InlineKeyboardButton("Да", callback_data='click'))

markup_question_2 = ReplyKeyboardMarkup(resize_keyboard=True)
markup_question_2.add(KeyboardButton("Мяч"))
markup_question_2.add(KeyboardButton("Лыжи"))
markup_question_2.add(KeyboardButton("Развивающие игры"))

markup_question_3 = ReplyKeyboardMarkup(resize_keyboard=True)
markup_question_3.add(KeyboardButton("Техника и тактика"))
markup_question_3.add(KeyboardButton("Сила и выносливость"))
markup_question_3.add(KeyboardButton("Другое"))

markup_question_4 = ReplyKeyboardMarkup(resize_keyboard=True)
markup_question_4.add(KeyboardButton("Провести время"))
markup_question_4.add(KeyboardButton("Силове показатели"))
markup_question_4.add(KeyboardButton("Мышление"))

markup_question_5 = ReplyKeyboardMarkup(resize_keyboard=True)
markup_question_5.add(KeyboardButton("Проф. спорт"))
markup_question_5.add(KeyboardButton("Поддержание формы"))
markup_question_5.add(KeyboardButton("Чем-то занять"))


@bot.message_handler(commands=['start'])
def send_start(message: Message):
    # создаю запись о пользаватели в json файле
    if str(message.chat.id) not in data_users:
        # создаю пользователя в json
        data_users[str(message.chat.id)] = {"name": message.from_user.first_name, "progress": 0, "summer_sports": 0,
                                            "winter_sports": 0, "other": 0}
    # сохраняем данные в json
    save_data(data_users)
    text = (
        f"Вероятно, ты знаешь, что некоторые виды спорта могут быть несовместимы с определенными физическими характеристиками или состояниями человека.\n"
        f"Этот бот создан с целью помочь тебе сделать правильный выбор.🏋‍♂️🚵‍♀️🤸")
    bot.send_message(chat_id=message.chat.id, text=text)
    bot.send_message(chat_id=message.chat.id, text="Готов начинать?", reply_markup=keyboard_1)


@bot.message_handler(commands=["help"])
def send_help(message: Message):
    text = (
        f"Чтож раз ты тут, видимо тебе понадобилась помощь🫠.\n\n"
        f"Тебе 🫵 предстоит ответить на ряд вопроссов связанных со спортом, не пытайся обдумывать каждый вопрос, просто отвечай интуитивно, и тогда результаты опроса будут максимально корректны⭐.\n\n"
        f"В конце опроса, я выведу результат какой вид спорта подойдёт именно тебе.\n\n"
        f"Если ты вдруг решишь прервать тест, всегда можешь вернуться, и мы начнём с тобой, где остановились. Согласись приятно,когда не нужно перепрохадить всё по сто тысяч раз😅. Для этого, просто когда вернешься используй /return\n\n"
        f"Что бы взаимодействовать со мной используй встроенную клавиатуру, так я смогу понимать тебя😉.\n"
    )
    bot.send_message(chat_id=message.chat.id, text=text)


# создаю ключи для ответов. Если в тексте появляется один из ключей, отправляется следующий хендлер
def filter_answer1(message: Message):
    keywords = ["Команада", "Одиночные", "Затрудняюсь ответить"]
    return message.text in keywords


def filter_answer2(message: Message):
    keywords = ["Мяч", "Лыжи", "Развивающие игры"]
    return message.text in keywords


def filter_answer3(message: Message):
    keywords = ["Техника и тактика", "Сила и выносливость", "Другое"]
    return message.text in keywords


def filter_answer4(message: Message):
    keywords = ["Провести время", "Силове показатели", "Мышление"]
    return message.text in keywords


def filter_answer5(message: Message):
    keywords = ["Проф. спорт", "Поддержание формы", "Чем-то занять"]
    return message.text in keywords


def filter_return(message: Message):
    keywords = "⤵️Продолжить⤵️"
    return message.text in keywords


# так как инлайн кнопка, клавиатуру создаю внутри хндлера и делаю ее глобальной для функции stop
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    if call.data == 'click':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="✅✅✅",
                              reply_markup=InlineKeyboardMarkup())
        # обнуляю все переменные, на тот случай, если пользователь во время теста решит начать заново, и эти переменнеы не ушли за свои пределы.
        # обнуляю в первом вопроссе, а не в старте, по причине того, что пользователю когда решит удалить чат, придется нажать start что бы добраться до функцуии возращения.
        data_users[str(call.message.chat.id)]["summer_sports"] = 0
        data_users[str(call.message.chat.id)]["winter_sports"] = 0
        data_users[str(call.message.chat.id)]["other"] = 0
        data_users[str(call.message.chat.id)]["progress"] = 0
        save_data(data_users)
        global markup_question_1
        markup_question_1 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup_question_1.add(KeyboardButton("Команада"))
        markup_question_1.add(KeyboardButton("Одиночные"))
        markup_question_1.add(KeyboardButton("Затрудняюсь ответить"))
        data_users[str(call.message.chat.id)]["progress"] += 1
        # отправляю вопроссы с ответами из файла info
        text = survey[0]["question"]
        sleep(1)
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup_question_1)
        text2 = survey[0]["answers"]
        bot.send_message(chat_id=call.message.chat.id, text=text2, reply_markup=markup_question_1)
        save_data(data_users)


@bot.message_handler(content_types=['text'],
                     func=filter_answer1)  # если хендлер заметит нужный ключ, он сработает. 1 хендлер запускался от кнопки.
def send_answer2(message: Message):
    text = survey[1]["question"]
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup_question_2)
    text2 = survey[1]["answers"]
    bot.send_message(chat_id=message.chat.id, text=text2, reply_markup=markup_question_2)
    # Начисляю баллы за ответ + прогресс.
    data_users[str(message.chat.id)]["progress"] += 1
    if message.text == "Команада":
        data_users[str(message.chat.id)]["summer_sports"] += 1
    elif message.text == "Одиночные":
        data_users[str(message.chat.id)]["winter_sports"] += 1
    elif message.text == "Затрудняюсь ответить":
        data_users[str(message.chat.id)]["other"] += 1
    save_data(data_users)


@bot.message_handler(content_types=['text'], func=filter_answer2)
def send_answer3(message: Message):
    text = survey[2]["question"]
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup_question_3)
    text2 = survey[2]["answers"]
    bot.send_message(chat_id=message.chat.id, text=text2, reply_markup=markup_question_3)
    data_users[str(message.chat.id)]["progress"] += 1
    save_data(data_users)
    if message.text == "Мяч":
        data_users[str(message.chat.id)]["summer_sports"] += 1
    elif message.text == "Лыжи":
        data_users[str(message.chat.id)]["winter_sports"] += 1
    elif message.text == "Развивающие игры":
        data_users[str(message.chat.id)]["other"] += 1
    save_data(data_users)


@bot.message_handler(content_types=["text"], func=filter_answer3)
def send_answer4(message: Message):
    text = survey[3]["question"]
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup_question_4)
    text2 = survey[3]["answers"]
    bot.send_message(chat_id=message.chat.id, text=text2, reply_markup=markup_question_4)
    data_users[str(message.chat.id)]["progress"] += 1
    save_data(data_users)
    if message.text == "Техника и тактика":
        data_users[str(message.chat.id)]["summer_sports"] += 1
    elif message.text == "Сила и выносливость":
        data_users[str(message.chat.id)]["winter_sports"] += 1
    elif message.text == "Другое":
        data_users[str(message.chat.id)]["other"] += 1
    save_data(data_users)


@bot.message_handler(content_types=["text"], func=filter_answer4)
def send_answer5(message: Message):
    text = survey[4]["question"]
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup_question_5)
    text2 = survey[4]["answers"]
    bot.send_message(chat_id=message.chat.id, text=text2, reply_markup=markup_question_5)
    data_users[str(message.chat.id)]["progress"] += 1
    save_data(data_users)
    if message.text == "Провести время":
        data_users[str(message.chat.id)]["summer_sports"] += 1
    elif message.text == "Силове показатели":
        data_users[str(message.chat.id)]["winter_sports"] += 1
    elif message.text == "Мышление":
        data_users[str(message.chat.id)]["other"] += 1
    save_data(data_users)


@bot.message_handler(content_types=["text"], func=filter_answer5)
def send_result(message: Message):
    if message.text == "Проф. спорт":
        data_users[str(message.chat.id)]["summer_sports"] += 1
    elif message.text == "Поддержание формы":
        data_users[str(message.chat.id)]["winter_sports"] += 1
    elif message.text == "Чем-то занять":
        data_users[str(message.chat.id)]["other"] += 1
    save_data(data_users)
    # Проверяю какая шкала набрала больше баллов, и в зависимости от этого, присылаю результат из файла info и фотографии из папки media.
    if data_users[str(message.chat.id)]["summer_sports"] > data_users[str(message.chat.id)]["winter_sports"] and \
            data_users[str(message.chat.id)]["summer_sports"] > data_users[str(message.chat.id)]["other"]:
        with open('media/f.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        with open('media/x.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        bot.send_message(chat_id=message.chat.id, text=result[0], reply_markup=ReplyKeyboardRemove())
    elif data_users[str(message.chat.id)]["winter_sports"] > data_users[str(message.chat.id)]["summer_sports"] and \
            data_users[str(message.chat.id)]["winter_sports"] > data_users[str(message.chat.id)]["other"]:
        with open('media/a.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        with open('media/t.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        bot.send_message(chat_id=message.chat.id, text=result[1], reply_markup=ReplyKeyboardRemove())
    elif data_users[str(message.chat.id)]["other"] > data_users[str(message.chat.id)]["summer_sports"] and \
            data_users[str(message.chat.id)]["other"] > data_users[str(message.chat.id)]["winter_sports"]:
        with open('media/h.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        with open('media/k.jpg', 'rb') as img:
            bot.send_photo(message.chat.id, img)
        bot.send_message(chat_id=message.chat.id, text=result[2], reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=message.chat.id, text=result[3],
                         reply_markup=ReplyKeyboardRemove())  # reply_markup=ReplyKeyboardRemove() удаляю пользователю клавиатуру.
    # Обнуляю шкалы.
    data_users[str(message.chat.id)]["summer_sports"] = 0
    data_users[str(message.chat.id)]["winter_sports"] = 0
    data_users[str(message.chat.id)]["other"] = 0
    data_users[str(message.chat.id)]["progress"] = 0
    save_data(data_users)
    sleep(3)
    bot.send_message(message.chat.id, text="Если хочешь пройти тест ещё раз, жми /start 🚀")


# Остановка опросса.
@bot.message_handler(commands=["return"])
def send_return(message: Message):
    markup_stop = ReplyKeyboardMarkup(resize_keyboard=True)
    markup_stop.add("⤵️Продолжить⤵️")
    text = "Вы продожите прошлое анкетирование🤔?"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup_stop)


@bot.message_handler(content_types=["text"], func=filter_return)
def send_continue(message: Message):
    # проверяю в зависимотси от вопросса какую клавиатуру прислать пользователю.
    if message.text == "⤵️Продолжить⤵️":
        data_users[str(message.chat.id)]["progress"] -= 1
        if data_users[str(message.chat.id)]["progress"] == 0:
            markup = markup_question_1
        elif data_users[str(message.chat.id)]["progress"] == 1:
            markup = markup_question_2
        elif data_users[str(message.chat.id)]["progress"] == 2:
            markup = markup_question_3
        elif data_users[str(message.chat.id)]["progress"] == 3:
            markup = markup_question_4
        elif data_users[str(message.chat.id)]["progress"] == 4:
            markup = markup_question_5
        elif data_users[str(message.chat.id)]["progress"] < 0:
            bot.send_message(chat_id=message.chat.id, text="🚥Вы еще не начинали прохождение теста, нажмите /start 🚥")
        # Присылаю вопросс на котором остановился пользователь
        text1 = survey[data_users[str(message.chat.id)]["progress"]]["question"]
        bot.send_message(chat_id=message.chat.id, text=text1, reply_markup=markup)
        text2 = survey[data_users[str(message.chat.id)]["progress"]]["answers"]
        bot.send_message(chat_id=message.chat.id, text=text2, reply_markup=markup)
        data_users[str(message.chat.id)]["progress"] += 1


@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'text', 'location', 'contact', 'sticker'])
def send_echo(mesage: Message):
    text = (f"Вы отправили ({mesage.text}).\n"
            f"Но к сожалению я вас не понял😔, для общения со мной используйте встроенные кнопки.🤗")
    bot.send_message(chat_id=mesage.chat.id, text=text)


bot.infinity_polling()
