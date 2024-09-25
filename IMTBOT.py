import telebot
from telebot import types

bot = telebot.TeleBot('7515324386:AAEsjEOUAXwPY-BDD8RiiY72QMRRk_f-d60')

#Хранение
user_data = {}

# Старт
@bot.message_handler(commands=['start'])
def start(message):
    # Кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('🍊 Диетолог')
    b2 = types.KeyboardButton('⚖️ ИМТ ')
    b3 = types.KeyboardButton('💵 Поддержка')
    b4 = types.KeyboardButton('🆘 Помощь')

    markup.add(b1, b2, b3, b4)
    # Приветствие
    bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}! \nЯ здесь, чтобы помочь вам рассчитать <b>индекс массы тела</b>.'.format(message.from_user),reply_markup=markup, parse_mode='html')

# Обработка меню
@bot.message_handler(func=lambda message: message.text == '⚖️ ИМТ')
def ask_weight(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш вес в кг (например, 70):")
    bot.register_next_step_handler(message, get_weight)

# Получаем вес
def get_weight(message):
    try:
        weight = float(message.text)
        user_data[message.chat.id]['weight'] = weight
        bot.send_message(message.chat.id, "Теперь введите ваш рост в сантиметрах (например, 170):")
        bot.register_next_step_handler(message, get_height)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное значение веса (только число).")
        bot.register_next_step_handler(message, get_weight)

# Получаем рост
def get_height(message):
    try:
        height_cm = float(message.text)
        height_m = height_cm / 100  # Преобразуем сантиметры в метры
        user_data[message.chat.id]['height'] = height_m
        calculate_bmi(message)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное значение роста (только число).")
        bot.register_next_step_handler(message, get_height)

# Рассчитываем и отправляем ИМТ
def calculate_bmi(message):
    weight = user_data[message.chat.id]['weight']
    height = user_data[message.chat.id]['height']
    try:
        bmi = weight / (height ** 2)
        bot.send_message(message.chat.id, f'Ваш индекс массы тела: {bmi:.2f}')
        if bmi <= 18.5:
            bot.send_message(message.chat.id, '\n<b>У Вас недовес массы тела </b>. С недовесом вам стоит обратить внимание на следующие рекомендации: \n'
                              '❗️<b>Питание:</b> увеличьте калорийность рациона за счёт здоровых продуктов, богатых питательными веществами. Регулярно употребляйте разнообразные фрукты, овощи, цельнозерновые продукты, бобовые, орехи и семена.\n '
                              '❗️<b>Физическая активность:</b> начните с лёгких упражнений, постепенно увеличивая интенсивность и продолжительность тренировок. Стремитесь к умеренной физической активности не менее 30 минут в день, 5 дней в неделю. \n'
                              '❗️<b>Здоровый сон:</b> обеспечьте себе полноценный сон не менее 7–8 часов в сутки.\n'
                              '❗️<b>Управление стрессом:</b> практикуйте техники релаксации, такие как медитация, глубокое дыхание или йога.\n'
                              '❗️<b>Регулярные медицинские осмотры:</b> следите за своим здоровьем, регулярно посещайте врача для контроля состояния и получения рекомендаций.\n'
                              '❗️<b>НАПОМИНАЕМ! Этот бот создан чтобы узнавать индекс массы тела. Следует сходить к квалифицированному диетологу!</b>', parse_mode='html')
        elif 18.5 < bmi <= 24.9:
            bot.send_message(message.chat.id, '\n<b>У Вас норма массы тела.</b>\n '
                              '❗️С нормальным индексом массы тела вам нужно продолжать поддерживать здоровый образ жизни, включающий сбалансированное питание и регулярную физическую активность.\n'
                              '❗️Старайтесь придерживаться разнообразного рациона, богатого фруктами, овощами, белками, полезными жирами и сложными углеводами. Не забывайте о важности воды для поддержания гидратации организма.\n '
                              '❗️Регулярные физические упражнения помогут укрепить здоровье и улучшить общее самочувствие. \n'
                              '❗️Продолжайте следить за качеством сна и уровнем стресса, поскольку они также влияют на ваше физическое и психическое состояние.\n'
                              '❗️<b>НАПОМИНАЕМ! Этот бот создан чтобы узнавать индекс массы тела. Следует сходить к квалифицированному диетологу!</b>', parse_mode='html')
        else:
            bot.send_message(message.chat.id, '\nУ Вас избыток массы тела. С перевесом вам стоит принять следующие меры:\n'
                                  '❗️<b> Питание:</b> сократите потребление высококалорийных продуктов, увеличьте потребление овощей, фруктов, цельнозерновых продуктов и белковой пищи. Ограничьте размер порций. \n'
                                  '❗️<b> Физическая активность:</b> начните с умеренных физических нагрузок, постепенно увеличивайте интенсивность и продолжительность тренировок. Стремитесь к умеренной физической активности не менее 150 минут в неделю.\n'
                                  '❗️<b> Здоровый сон:</b> обеспечьте себе полноценный сон не менее 7–8 часов в сутки.\n'
                                  '❗️<b> Управление стрессом:</b> практикуйте техники релаксации, такие как медитация, глубокое дыхание или йога.\n'
                                  '❗️<b> Регулярные медицинские осмотры:</b> следите за своим здоровьем, регулярно посещайте врача для контроля состояния и получения рекомендаций.\n'
                                  '❗️<b>НАПОМИНАЕМ! Этот бот создан чтобы узнавать индекс массы тела. Следует сходить к квалифицированному диетологу!</b>', parse_mode='html')
    except ZeroDivisionError:
        bot.send_message(message.chat.id, 'Ошибка при расчете. Пожалуйста, введите корректные данные.')

#Обработка других кнопок
@bot.message_handler(func=lambda message: not message.text.startswith('/imt'), content_types=['text'])
def bot_message(message):
    if message.text == '🍊 Диетолог':
        diet(message)
    elif message.text == '🆘 Помощь':
        pom(message)
    elif message.text == '💵 Поддержка':
        donate(message)
# Донат меню
def donate(message):
    bot.send_message(message.chat.id, 'Спасибо что решили поддержать нас денежно! ЮMoney (4100 1178 5920 9750)')

# Диета в меню
def diet(message):
    bot.send_message(message.chat.id, 'У нас нет диетолога, но вы могли бы взять рекламу у нас!')

# Помощь
@bot.message_handler(commands=['pom'])
def pom(message):
    bot.send_message(message.chat.id, 'Если возникли проблемы, пишите на почту: imt.bot.gr@gmail.com')

bot.polling(none_stop=True)