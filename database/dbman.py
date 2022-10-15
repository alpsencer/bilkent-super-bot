# DBMan - Database Management Functions
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes


def add_user(update: Update):
    # Adding user to the info database
    user = update.message.from_user
    db = sqlite3.connect("database/main.sqlite")

    im = db.cursor()
    im.execute("""CREATE TABLE IF NOT EXISTS 
        info (username, id INTEGER UNIQUE, full_name, first_name, last_name, language_code) """)
    username = str(user.name)
    user_id = str(user.id)
    user_full_name = str(user.full_name)
    user_first_name = str(user.first_name)
    user_last_name = str(user.last_name)
    user_language_code = str(user.language_code)


    im.execute("""INSERT OR IGNORE INTO info
        (username, id, full_name, first_name, last_name, language_code) values(?,?,?,?,?,?)""", (username, user_id,user_full_name, user_first_name, user_last_name,user_language_code))

    db.commit()

    db.close()

    # Adding user to the counter database
    db = sqlite3.connect("database/main.sqlite")

    im = db.cursor()
    im.execute("""CREATE TABLE IF NOT EXISTS 
        counter (username, id INTEGER UNIQUE, ct_start, ct_start_over, ct_dining, ct_au_meal,ct_ma_meal,ct_weekly_meal) """)
    username = str(user.name)
    user_id = str(user.id)
    ct_start = 0
    ct_start_over = 0
    ct_dining = 0
    ct_au_meal = 0
    ct_au_meal = 0
    ct_ma_meal = 0
    ct_weekly_meal = 0

    im.execute("""INSERT OR IGNORE INTO counter
        (username, id,ct_start,ct_start_over,ct_dining,ct_au_meal,ct_ma_meal,ct_weekly_meal) values(?,?,?,?,?,?,?,?)""", (username, user_id,ct_start, ct_start_over, ct_dining,ct_au_meal,ct_ma_meal,ct_weekly_meal))

    db.commit()

    db.close()

def ct_start(update: Update):
    # Increases user's ct_start_over_count
    user = update.message.from_user
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_start = ct_start + 1 WHERE id LIKE {user.id} """    
    
    im.execute(query)

    db.commit()
    db.close()

def ct_start_over(context: ContextTypes.DEFAULT_TYPE):
    # Increases user's ct_start_over_count
    id = context._chat_id
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_start_over = ct_start_over + 1 WHERE id LIKE {id} """    
    
    im.execute(query)

    db.commit()
    db.close()

def ct_dining(context: ContextTypes.DEFAULT_TYPE):
    # Increases user's ct_start_over_count
    id = context._chat_id
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_dining = ct_dining + 1 WHERE id LIKE {id} """    
    
    im.execute(query)

    db.commit()
    db.close()

def ct_au_meal(context: ContextTypes.DEFAULT_TYPE):
    # Increases user's ct_start_over_count
    id = context._chat_id
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_ma_meal = ct_ma_meal + 1 WHERE id LIKE {id} """    
    
    im.execute(query)

    db.commit()
    db.close()

def ct_ma_meal(context: ContextTypes.DEFAULT_TYPE):
    # Increases user's ct_start_over_count
    id = context._chat_id
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_ma_meal = ct_ma_meal + 1 WHERE id LIKE {id} """    
    
    im.execute(query)

    db.commit()
    db.close()

def ct_weekly_meal(context: ContextTypes.DEFAULT_TYPE):
    # Increases user's ct_start_over_count
    id = context._chat_id
    db = sqlite3.connect("database/main.sqlite")
    im = db.cursor()
    query = f"""UPDATE counter SET ct_weekly_meal = ct_weekly_meal + 1 WHERE id LIKE {id} """    
    
    im.execute(query)

    db.commit()
    db.close()