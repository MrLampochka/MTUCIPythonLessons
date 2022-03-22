import telebot
from telebot import types

import random
import config
import codecs

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width=1)
    
    keyboard.add("Список группы","Список преподавателей","Расписание занятий")
    bot.send_message(message.chat.id, 'Привет! Выбери необходимые списки:', reply_markup=keyboard)
    
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею показывать спискок студентов группы и преподавателей группы БСС1901:')
    
@bot.message_handler(commands=['authorinfo'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я, Хакимов Валентин Маратович, студент группы БСС1901\
    \nhttps://t.me/mr_lampochka')
    
@bot.message_handler(commands=['randnum'])
def start_message(message):
    bot.send_message(message.chat.id, f'Случайное число: {(random.randint(1,10))}')
    
countwords = {}
    
@bot.message_handler(commands=['countwords'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Введите предложение: ')
    bot.register_next_step_handler(msg, sentence)  
         
def sentence(message):
    try:
        countwords['text'] = message.text
        msg = bot.send_message(message.chat.id, 'Введите слово для поиска: ')
        bot.register_next_step_handler(msg, word)
    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Введите предложение: ')
        bot.register_next_step_handler(msg, sentence)

def word(message):
    try:
        countwords['word'] = message.text
        msg = bot.send_message(message.chat.id, f'Количество слов в тексте: {countwords.get("text").lower().count(countwords.get("word").lower())}') 
    except Exception as e:
        msg = bot.send_message(message.chat.id, 'Введите слово для поиска: ')
        bot.register_next_step_handler(msg, word)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "список преподавателей":
        bot.send_message(message.chat.id, codecs.open('lists/teachers.txt',"r","utf_8_sig").read())
        
    if message.text.lower() == "список группы":
        bot.send_message(message.chat.id, codecs.open('lists/students.txt',"r","utf_8_sig").read())

    if message.text.lower() == "расписание занятий":
        calKeyboard = types.InlineKeyboardMarkup(row_width=1)
        calKeyboard.add(types.InlineKeyboardButton("Открыть календарь в браузере","https://calendar.google.com/calendar/embed?src=0u5m9nrf6m0rcli0pe6n2ljl4s%40group.calendar.google.com&ctz=Europe%2FMoscow"),\
            types.InlineKeyboardButton("Подписаться на календарь (iCal)","https://calendar.google.com/calendar/ical/0u5m9nrf6m0rcli0pe6n2ljl4s%40group.calendar.google.com/public/basic.ics"))
        bot.send_photo(message.chat.id, open("lists/cal.png",'rb'),reply_markup=calKeyboard, caption="Расписание занятий группы БСС1901")

bot.infinity_polling()