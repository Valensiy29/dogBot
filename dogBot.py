# Press the green button in the gutter to run the script.
import telebot
import logging
import random
import re
import json
import requests
import pandas as pd
import os




DOG_1 = 'Как ты стал хорошим мальчиком?'
DOG_2 = 'Как стать псом?'
DOG_ALPHAVIT_1 = ['Гав','Мне пуфик','Арбуз попа ананас?','Тяв тяв','Рррррррр гав рав гав гав!',]
DOG_ALPHAVIT_2 = ['Пока псинка','Рад знакомству , пес мой меньший','Гав?']
random_message_1 = lambda: random.choice(DOG_ALPHAVIT_1)
random_message_2 = lambda: random.choice(DOG_ALPHAVIT_2)
TO_CHAT_ID = 266119831


# добавим логирование
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)



#импортируем токены
try:
    token = os.environ['TOKEN']
except:
    from private.token import token

# импортируем id админа
try:
    admin_id = os.environ['TG_ADMIN_ID']
except:
    from private.token import admin_id

try:
    token = os.environ['TOKEN']# в первую очередь импорт из системных переменных
except:
    from private.token import token# потом из этого файла

bot = telebot.TeleBot(token=token)



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_1 = telebot.types.KeyboardButton(text = 'Привет!')
    markup.add(key_1)
    bot.send_message(message.from_user.id, text='Привет , {0.first_name}! \nЯ разговорчивый пес , меня взял из приюта Valensiy.'.format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['text'])
def get_text_message(message):
    bot.message_handler(content_type=['text', 'document', 'audio'])
    if message.text == 'Привет!':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_2 = telebot.types.KeyboardButton(text='Стать псом!')
        key_3 = telebot.types.KeyboardButton(text=DOG_1)
        key_4 = telebot.types.KeyboardButton(text=DOG_2)
        key_5 = telebot.types.KeyboardButton(text='Помоги браткам!')
        key_6 = telebot.types.KeyboardButton(text='Помочь пёсилю выбрать друга')
        key_7 = telebot.types.KeyboardButton(text='Мне идти выгуливать псинку?')
        markup.add(key_2, key_3, key_4, key_5,key_6,key_7)
        bot.send_message(message.from_user.id, text=random_message_2() , reply_markup=markup)
    elif message.text == 'Стать псом!':
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_1 = telebot.types.InlineKeyboardButton(text='Я песина.', callback_data='1')
        keyboard.add(key_1)
        key_2 = telebot.types.InlineKeyboardButton(text='Я хочу стать псом.', callback_data='2')
        keyboard.add(key_2)
        bot.send_message(message.from_user.id, text='Ты кто по жизни вообще?', reply_markup=keyboard)
    elif message.text == 'Помоги браткам!':
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_1 = telebot.types.InlineKeyboardButton(text='Нажми на кнопку и помоги моим браткам!',url='http://www.priut.ru/', callback_data='3')
        keyboard.add(key_1)
        bot.send_message(message.from_user.id, text='Поможешь?', reply_markup=keyboard)
    elif message.text == 'Сам пес':
        bot.send_message(message.chat.id, 'Гав гав')
    elif message.text == DOG_1:
        bot.send_message(message.chat.id, 'Пора поведать тебе одну притчу,пес мой...\n '
                                          'когда я был ещё маленькой собачкой и путишествовал с большим псом и с собачёнкой \nмы посещали прекрасный город который запомниться мне надолго. '
                                          '\nКак и во многих городах я твердил что перееду в него и при заселении в будку я вёл себя прекрасно.В ту ночь я долго,долго...Булькал!'
                                          '\nИ вот , на утренней прогулке по городу в одном прекрасном месте меня наградил таким прозвищем большой пес.')
    elif message.text == DOG_2:
        bot.send_message(message.chat.id, 'Молчи.Китикэтовый.')
    elif message.text == "Мне идти выгуливать псинку?":
        try:
            weather_token = os.environ['WEATHER_TOKEN']
        except:
            from private.weather_token import weather_token
        url = 'http://api.weatherstack.com/current'
        params = {
            'access_key': weather_token,
            'query': 'Moscow'
            # , 'language':'Russian'
        }
        result_1 = json.loads(requests.get(url, params).text, strict=False)
        bot.send_message(message.chat.id, result_1['current'])
        temp_df = pd.read_csv(r'C:\Users\Valensiy\PycharmProjects\teleBot\docs\Multilingual_Weather_Conditions(1).csv', sep=',', encoding='utf-8')
        temp_response = f"{result_1['current']['weather_icons']}, {result_1['location']['name']} : {temp_df[(temp_df.lang_name == 'Russian') & (temp_df.overhead_code == result_1['current']['weather_code'])].trans_text_day.values[0]}" \
                        f"температура: {result_1['current']['temperature']}, скорость ветра: {result_1['current']['wind_speed']}, атмосферное давление: {result_1['current']['pressure']}"
        bot.send_message(message.chat.id,text=temp_response)
    elif message.text == 'Помочь пёсилю выбрать друга':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первый красавчик')
        key_2 = telebot.types.KeyboardButton(text='Второго я бы съел')
        key_3 = telebot.types.KeyboardButton(text='Бери третьего')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1,key_2,key_3,key_4)
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\1.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\2.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id,text = 'Помоги братка выбрать.',reply_markup=markup)
    elif message.text == 'Первый красавчик':
        bot.send_message(message.chat.id,text='Он какой-то злой(((')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая красивая')
        key_2 = telebot.types.KeyboardButton(text='Со второй все будут думать что пес важный')
        key_3 = telebot.types.KeyboardButton(text='Третья для обычного паренька')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_1.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_2.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Выбери пёсрине штутчку,только удобную.",reply_markup=markup)
    elif message.text == 'Второго я бы съел':
        bot.send_message(message.chat.id,text='Пацанчик на спортике , вкусный наверно.')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая красивая')
        key_2 = telebot.types.KeyboardButton(text='Со второй все будут думать что пес важный')
        key_3 = telebot.types.KeyboardButton(text='Третья для обычного паренька')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_1.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_2.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Выбери пёсрине штутчку,только удобную.",reply_markup=markup)
    elif message.text == 'Бери третьего':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая красивая')
        key_2 = telebot.types.KeyboardButton(text='Со второй все будут думать что пес важный')
        key_3 = telebot.types.KeyboardButton(text='Третья для обычного паренька')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        bot.send_message(message.chat.id, text='Пусси бой какой-то.')
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_1.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_2.jpg','rb' ) as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\povodok_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Выбери пёсрине штутчку,только удобную.",reply_markup=markup)
    elif message.text == 'Первая красивая':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая вкусная клык даю')
        key_2 = telebot.types.KeyboardButton(text='Второй я бы сам питался')
        key_3 = telebot.types.KeyboardButton(text='Третьей штучечкой')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        bot.send_message(message.chat.id, text='пон')
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_1.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_2.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Чем пёсрина будет питаться решать тоже тебе", reply_markup=markup)
    elif message.text == 'Со второй все будут думать что пес важный':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая вкусная клык даю')
        key_2 = telebot.types.KeyboardButton(text='Второй я бы сам питался')
        key_3 = telebot.types.KeyboardButton(text='Третьей штучечкой')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        bot.send_message(message.chat.id, text='Гламурненькая штучкечка')
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_1.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_2.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Чем пёсрина будет питаться решать тоже тебе", reply_markup=markup)
    elif message.text == "Третья для обычного паренька":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Первая вкусная клык даю')
        key_2 = telebot.types.KeyboardButton(text='Второй я бы сам питался')
        key_3 = telebot.types.KeyboardButton(text='Третьей штучечкой')
        key_4 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1, key_2, key_3,key_4)
        bot.send_message(message.chat.id, text='Нормик')
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_1.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_2.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        with open(r'C:\Users\Valensiy\PycharmProjects\teleBot\images\korm_3.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode="HTML")
        bot.send_message(message.chat.id, text="Чем пёсрина будет питаться решать тоже тебе", reply_markup=markup)
    elif message.text == 'Первая вкусная клык даю':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1)
        bot.send_message(message.chat.id, text="Ээээ брат ты только номер своей лялякалки дай", reply_markup=markup)
    elif message.text == 'Второй я бы сам питался':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1)
        bot.send_message(message.chat.id, text="Ээээ брат ты только номер своей лялякалки дай", reply_markup=markup)
    elif message.text == 'Третьей штучечкой':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = telebot.types.KeyboardButton(text='Вернуться в главное меню')
        markup.add(key_1)
        bot.send_message(message.chat.id, text="Ээээ брат ты только номер своей лялякалки дай", reply_markup=markup)
    elif message.text == 'Вернуться в главное меню':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_2 = telebot.types.KeyboardButton(text='Стать псом!')
        key_3 = telebot.types.KeyboardButton(text=DOG_1)
        key_4 = telebot.types.KeyboardButton(text=DOG_2)
        key_5 = telebot.types.KeyboardButton(text='Помоги браткам!')
        key_6 = telebot.types.KeyboardButton(text='Помочь пёсилю выбрать друга')
        key_7 = telebot.types.KeyboardButton(text='Мне идти выгуливать псинку?')
        markup.add(key_2, key_3, key_4, key_5, key_6, key_7)
        bot.send_message(message.chat.id,text='Гав?',reply_markup=markup)
    else:
        string = message.text
        result_2 = re.findall(r'\d([0-9]{10})|\d([0-9]{9})', string)
        phone_number = ""
        if len(result_2) > 0:
            for i in result_2[-1]:
                if str(i).isnumeric():
                    phone_number = i
                    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
                    bot.send_message(message.chat.id, text=f'Вот цифра твой: {phone_number}')
                    bot.send_message(message.chat.id,text='Заказ выбран и передан в обработку. В ближайшее время с вами свяжется менеджер')
        if not phone_number:
            bot.send_message(message.chat.id, text='Ты чё мне чурчхелу какую то прислал!')



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "1":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, text=random_message_1())# код сохранения данных, или их обработки
    elif call.data == '2':
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_1 = telebot.types.InlineKeyboardButton(text='Пройти курс по пёсо развитию',url='https://lp.kinologschool.ru/')
        keyboard.add(key_1)
        bot.send_message(call.message.chat.id, text='Вашему псу нужно пройти курс по пёсо развитию:', reply_markup=keyboard)



if __name__ == '__main__':
    print('{:*^100}'.format(' bot started polling '))
    bot.polling(none_stop=True, interval=0)