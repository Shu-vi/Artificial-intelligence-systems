from deeppavlov import build_model
from deeppavlov.core.common.file import read_json
from enum import Enum
import requests
import telebot
import json


class Modes(Enum):
    INITIAL = 1
    QUESTINGANSWERING = 2


user_states = {}

token = open("token.txt").readline().strip()
bot = telebot.TeleBot(token)

model_config_roberta = read_json("few_shot_roberta.json")
model_roberta = build_model(model_config_roberta, download=True)

dataset = []
with open('train.json', 'r') as file:
    dataset = json.load(file)


def cat_facts():
    url = "http://127.0.0.1:5001/"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return "Ошибка при попытке получить факт о коте"


def cat_img():
    url = "http://127.0.0.1:5000/"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return "Ошибка при попытке получить изображение кота"


def naruto(question):
    url = "http://127.0.0.1:5002/"
    data = {"data": question}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json()['data'])
        return response.json()['data']
    else:
        return "Ошибка при попытке узнать о вселенной Наруто"


@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    user_states[user_id] = Modes.INITIAL
    bot.reply_to(message, "Привет! Ты можешь спросить у меня о Наруто, попросить факт о кошках или картинку с котом. Просто попробуй попросить о чём-то.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.chat.id
    mode = user_states.get(user_id, Modes.INITIAL)
    intent = model_roberta([message.text], dataset)[0]
    if intent == "cat_facts" and mode == Modes.INITIAL:
        print("Ищу факт о котах")
        bot.reply_to(message, cat_facts())
    elif intent == "cat_img" and mode == Modes.INITIAL:
        print("Отправляю случайное изображение")
        bot.reply_to(message, cat_img())
    elif mode == Modes.QUESTINGANSWERING and intent != "init":
        print("Отвечаю на вопрос")
        bot.reply_to(message, naruto(message.text))
    elif intent == "naruto" and mode == Modes.INITIAL:
        print("Перехожу в режим ответа на вопросы")
        user_states[user_id] = Modes.QUESTINGANSWERING
        bot.reply_to(message, "Сейчас ты можешь начать задавать мне вопросы про вселенную Наруто. Когда тебе надоест и ты захочешь воспользоваться другими функциями, просто скажи Хватит")
    elif intent == "init" and mode == Modes.QUESTINGANSWERING:
        print("Выхожу из режима ответа на вопросы")
        user_states[user_id] = Modes.INITIAL
        bot.reply_to(
            message, "Сейчас мы можем снова вернуться к котикам. Если ты вышел из режима по ошибке, дай мне знать, что ты хочешь к нему вернуться")


bot.infinity_polling()
