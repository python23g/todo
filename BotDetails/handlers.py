from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import requests
from tinydb import TinyDB, Query
from .buttons import menu, users





def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Backendga post request jo'natish


    url = 'http://127.0.0.1:8000/api/v1/users/'
    response = requests.post(url, json={
        "username": user_id,
        "password": user_id
    })


    update.message.reply_html(
        text="Assalomu Aleykum botimizga xush kelibsiz!",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

    # Backenddan olingan ID ni foydalanib yangi so'rovlarni olish


    get_url = f'http://127.0.0.1:8000/api/v1/users/{user_id}/todos/'

    todo = requests.get(get_url)
    todos = todo.json()

    # Todo'larni chiqarish
    if todos:
       update.message.reply_text(todos) 
    else:
        update.message.reply_text("Sizning todolaringiz bo'sh.")

def userlar(update: Update, context: CallbackContext):

    update.message.reply_html(
        text="Pastdagi bo'limlardan birini tanlang",
        reply_markup=ReplyKeyboardMarkup(users, resize_keyboard=True)
    )

def todos(update: Update, context: CallbackContext):

    update.message.reply_html(
        text=f"Sizning Todolaringiz\n\n"
    )

def get_by_id(update: Update, context: CallbackContext):

    url = 'http://127.0.0.1:8000/api/v1/users/1'
    response = requests.get(url)
    response = response.json()