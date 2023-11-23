from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
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
    username = str(user_id)
    get_url = f'http://127.0.0.1:8000/api/v1/users/{username}/todos/'
    todo = requests.get(get_url)
    todos = todo.json()
    todo_list=[]
    # Todo'larni chiqarish
    if todos:
        for todo in todos:
            todo_list.append(todos[0]['title'])
        update.message.reply_text(f"Your Todos:\n{todo_list}", reply_markup=get_inline_keyboard())
    else:
        update.message.reply_text("Sizning todolaringiz bo'sh.", reply_markup=get_inline_keyboard())


def get_inline_keyboard():
    keyboard = [
        [InlineKeyboardButton("Add Todo", callback_data="add_todo")]
    ]
    return InlineKeyboardMarkup(keyboard)


def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "add_todo":
        # Here you can implement the logic to handle adding a new todo
        # For example, you can ask the user for the new todo text.
        context.bot.send_message(user_id, "Enter your new todo:")
        context.user_data['awaiting_todo'] = True


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