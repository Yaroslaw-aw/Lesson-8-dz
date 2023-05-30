import telebot
import requests
from telebot import types
import time



# Конвертация message.date в читабельный вид
convertDate = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

myFirstBot = telebot.TeleBot("6154888943:AAHkZBEyCJKP_KgzDyvB7PBIJoFgfKHXCJk")

markup = types.ReplyKeyboardMarkup(row_width=2)
btn_weather = types.KeyboardButton('Погода')
btn_cats = types.KeyboardButton('Котики')
btn_game = types.KeyboardButton('Игра')
btn_start = types.KeyboardButton('/start')
btn_question = types.KeyboardButton('Вопрос')
markup.add(btn_question, btn_weather, btn_cats, btn_game, btn_start)

bots_numbres: dict = {}
players_attempts: dict = {}

@myFirstBot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    user_id = str(message.from_user.id)
    user_name = str(message.from_user.first_name)
    reg_date = convertDate(message.date)

    myFirstBot.reply_to(message, 
                        "Привет, я умею показывать погоду, котиков и играть в игру 'угадай число', так же вы можете задать вопрос тех. поддержке.", reply_markup=markup)
    try:
        with open('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/id_list.txt', mode='r', encoding='utf-8') as id_list:
            ids = id_list.read().split('\n')
            ids = ids[:-1]
        if user_id not in ids:
            with open('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/id_list.txt', mode='a', encoding='utf-8') as id_list:
                id_list.write(f'{user_id}\n')
            with open('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/list_of_users.txt', mode='a', encoding='utf-8') as list_of_users:
                list_of_users.write(f'{user_id}, {user_name}, {reg_date}\n')
    except:
        with open('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/id_list.txt', mode='a', encoding='utf-8') as id_list:
                id_list.write(f'{user_id}\n')
        with open('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/list_of_users.txt', mode='a', encoding='utf-8') as list_of_users:
            list_of_users.write(f'{user_id}, {user_name}, {reg_date}\n')


@myFirstBot.message_handler(content_types=['text'])
def greetings(message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text: str = message.text.lower()

    if 'привет' in text:
        myFirstBot.reply_to(message, f'Привет, {user_name}!')

    elif 'погода' in text:
        req = requests.get('https://wttr.in/?0T')
        myFirstBot.reply_to(message, req.text)

    elif 'вопрос' in text:
        def question_from_user(message):
            text: str = message.text.lower()
            user_file = str(user_id) + '.txt'
            with open(f'C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/questions from users/{user_file}', mode='a', encoding='utf-8') as questions:                
                question_time = convertDate(message.date)
                questions.write(f'{user_id}; {question_time}; {user_name}; {text}\n')
                myFirstBot.send_message(user_id, 'Спасибо за Ваш вопрос, оператор ответит вам в ближайшее время')
        
        myFirstBot.send_message(user_id, 'Введите Ваш вопрос')   
        myFirstBot.register_next_step_handler(message, question_from_user) 
    elif 'котик' in text:
        try:
            req = requests.get('https://cataas.com/cat')    # https://http.cat/[status_code]
            myFirstBot.send_photo(user_id, req.content)
        except:
            myFirstBot.reply_to(message, 'К сожалению, котики сейчас не хотят, чтобы на них смотрели. Попробуйте на них посмотреть позже.')

    elif 'игра' in text:
        import random
        bots_numbres[user_id] = random.randint(1, 1000)
        players_attempts[user_id] = 0
        myFirstBot.reply_to(message, f'Я загадал случайное число от 1 до 1000.\n' + 
                            "Угадайте, какое?")
        
    else:
        if text.isdigit():

            attempt = int(message.text)

            if attempt == bots_numbres[user_id]:
                players_attempts[user_id] += 1
                myFirstBot.reply_to(message, f'Поздравляю, вы угадали!\nC {players_attempts[user_id]} попытки!')
                del players_attempts[user_id]
                del bots_numbres[user_id]
                print(players_attempts)

            elif attempt > bots_numbres[user_id]:
                players_attempts[user_id] += 1
                myFirstBot.reply_to(message, f'Загаданное число меньше')
                return players_attempts[user_id]
            
            elif attempt < bots_numbres[user_id]:
                players_attempts[user_id] += 1
                myFirstBot.reply_to(message, f'Загаданное число больше')
                return players_attempts[user_id]
            
        else:
            myFirstBot.reply_to(message, f'Вы ввели неверное число или неизвестную мне команду, попробуйте ещё раз.')

myFirstBot.polling()

def Mailing():
    with open ('C:/Users/User/Desktop/Lessons Programming/Stupid_python/Telegram bot/users/list_of_users.txt', mode='r', encoding='utf-8') as list_of_users:
        users = list_of_users.read().split('\n')
        users = users[:-1]
        for user in users:
            user = user.split(', ')
            myFirstBot.send_message(user[0], f'{user[1]}, здравствуйте! Это пока тестовая рассылка, ещё не ответы на вопросы ;)')
            
worker_bot = telebot.TeleBot("6127529328:AAFnhSRhBcj3Aed39nJtciURMeg7i-wBu7Q")

markup = types.ReplyKeyboardMarkup(row_width=2)
btn_mailing = types.KeyboardButton('Рассылка')
markup.add(btn_mailing)

@worker_bot.message_handler(commands=['start', 'help'])
def start_working(message):
    worker_bot.reply_to(message, 'Начало работы', reply_markup=markup)

@worker_bot.message_handler(content_types=['text'])
def Mail(message):

    text: str = message.text.lower()

    if 'рассылка' in text:
        print('Функция')
        Mailing()

worker_bot.polling()
