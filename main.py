"""
Bilkent Super Bot (Beta)
This bot provides many services to help 
Bilkent University students in daily school life.
V 0.2.0-beta

Author @alpsencer
"""

import datetime
from pathlib import Path
from datetime import date # To get day of the week
import os
import sqlite3

from cv2 import log
import pytz
from meal.capture.screenshot import takeScreenshot
from database import dbman

from telegram import __version__ as TG_VER
import logging

from dotenv import load_dotenv
load_dotenv()

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
START, DINING, SENDDAILYMENU, SENDWEEKLYMENU, OFFDINING, ONDINING, CALENDAR, LIBRARY, SPORT, SERVICES, COMMUNITIES, ABOUT, QUIT, SOON = range(14)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""

    # Adds user if does not exist
    dbman.add_user(update)
    # Function usage counter
    dbman.ct_start(update)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Dining Hall", callback_data=str(DINING)),
            InlineKeyboardButton("Academic Calendar", callback_data=str(SOON))
        ],
        [
            InlineKeyboardButton("Library", callback_data=str(SOON)),
            InlineKeyboardButton("Sport", callback_data=str(SOON)),
        ],
        [
            InlineKeyboardButton("Services", callback_data=str(SOON)),
            InlineKeyboardButton("Communities", callback_data=str(SOON)),
        ],
        [
            InlineKeyboardButton("About", callback_data=str(ABOUT)),
            InlineKeyboardButton("QUIT", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # Function usage counter
    dbman.ct_start_over(context)

    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Dining Hall", callback_data=str(DINING)),
            InlineKeyboardButton("Academic Calendar", callback_data=str(SOON))
        ],
        [
            InlineKeyboardButton("Library", callback_data=str(SOON)),
            InlineKeyboardButton("Sport", callback_data=str(SOON)),
        ],
        [
            InlineKeyboardButton("Services", callback_data=str(SOON)),
            InlineKeyboardButton("Communities", callback_data=str(SOON)),
        ],
        [
            InlineKeyboardButton("About", callback_data=str(ABOUT)),
            InlineKeyboardButton("QUIT", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Choose an option for me to help you:", reply_markup=reply_markup)
    return START_ROUTES


async def dining(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Settings about dining hall menu"""
    query = update.callback_query
    await query.answer()

    # Function usage counter
    dbman.ct_dining(context)

    keyboard = [
        [
            InlineKeyboardButton("Menu Of The Day", callback_data=str(SENDDAILYMENU)),
            InlineKeyboardButton("Menu Of The Week", callback_data=str(SENDWEEKLYMENU)),
        ],
        [
            InlineKeyboardButton("Turn on Daily Notifications", callback_data=str(ONDINING)),
            InlineKeyboardButton("Turn off Daily Notifications", callback_data=str(OFFDINING)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Settings about dining hall menu:", reply_markup=reply_markup
    )
    return START_ROUTES

async def sendDailyMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends menu of the day"""
    query = update.callback_query

    # Function usage counter
    dbman.ct_ma_meal(context)

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    
    
    day = date.today()
    weekDay = day.weekday()

    await query.message.reply_photo(
        photo=open(f"meal/daily-menus/ogle_{weekDay}.png", 'rb')  , caption = "Öğle Yemeği"
    )
    await query.message.reply_photo(
        photo=open(f"meal/daily-menus/aksam_{weekDay}.png", 'rb')  , caption = "Aksam Yemeği"
    )

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
         text="Başka bir işlem yapmak ister misiniz?", reply_markup=reply_markup
    )

    return END_ROUTES

async def sendWeeklyMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends menu of the week"""
    # FUNCTIONS WILL BE CHECKED TODO
    menu = "Weekly menu"
    query = update.callback_query
    await query.answer()

    # Function usage counter
    dbman.ct_weekly_meal(context)

    await query.message.reply_text(
        "Please wait this may take a few seconds"
    )
    await ss(context)
    await query.message.reply_photo(
        photo=open("meal/menu/weekly_menu.png", 'rb')  , caption = "Weekly Menu"
    )
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Menu Of The Week" , reply_markup=reply_markup
    )
    return END_ROUTES

async def onDiningNotifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Turns on notifications"""
    # FUNCTIONS WILL BE WRITTEN TODO
    # Enables Daily Meal Notifications
    await send_daily(update, context)
    
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Daily notifications turned on", reply_markup=reply_markup
    )
    return END_ROUTES

async def offDiningNotifications(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Turns off notifications"""
    # FUNCTIONS WILL BE WRITTEN TODO
    logger.info("OFF function started !!!!!!!!!!!")
    await unset(update, context)

    query = update.callback_query
    isRemovable = await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if(isRemovable):
        await query.edit_message_text(
            text="Daily notifications turned off", reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(
        text="Daily notifications is already turned off", reply_markup=reply_markup
        )
    
    return END_ROUTES

async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Calendar options"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("What's up this week?", callback_data=str(DINING)),
            InlineKeyboardButton("What's up this month?", callback_data=str(DINING)),
            InlineKeyboardButton("Turn on notifications?", callback_data=str(DINING)),
            InlineKeyboardButton("Turn off notifications?", callback_data=str(DINING)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def library(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(START)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """About the bot"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="""Bilkent Super Bot V 0.2.0-alpha \nBSB is <a href="https://github.com/alpsencer/bilkent-super-bot">Open Source 🥳</a> \nContributions are welcomed 😄\n<a href="https://www.linkedin.com/in/yavuzalpsencerozturk">Contact me 👨‍💻</a>""", parse_mode="HTML", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES

async def soon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Coming soon"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Main menu", callback_data=str(START)),
            InlineKeyboardButton("Quit", callback_data=str(QUIT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="This feature will be coming soon. Stay tuned.", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES



async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

# SCREENSHOT
async def ss(context: ContextTypes.DEFAULT_TYPE) -> None:
    takeScreenshot()
    

# DAILY MEAL NOTIFICATION FUNCTIONS
async def daily_notification(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    day = date.today()
    weekDay = day.weekday()

    # Function usage counter
    dbman.ct_au_meal(context)

    await context.bot.send_photo(job.chat_id,
        photo=open(f"meal/daily-menus/ogle_{weekDay}.png", 'rb')  , caption = "Öğle Yemeği"
    )
    await context.bot.send_photo(job.chat_id,
        photo=open(f"meal/daily-menus/aksam_{weekDay}.png", 'rb')  , caption = "Aksam Yemeği"
    )

async def send_daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    #t = datetime.time(22, 21,00)
    #now = datetime.datetime.now()

    # context.job_queue.run_once(alarm, datetime.time(hour=2, minute=31), chat_id=chat_id, name=str(chat_id), data=chat_id)

    ### ONCEKI YEMEK BILDIRIMLERI KALDIRILMALI !!!
    isRemoved = await remove_job_if_exists(str(chat_id), context)
    if(isRemoved):
        await context.bot.send_message(chat_id, "Daily meal notifications are already turned on")
    
    context.job_queue.run_daily(daily_notification, datetime.time(8, 00,00, tzinfo=pytz.timezone('Europe/Istanbul')), days = (0,1,2,3,4,5,6), chat_id=chat_id, name=str(chat_id),data=chat_id) 
    
    ## Duplicate of this code is in the notify on func
    #text = "Daily meal notifications are turned on"
    #await update.effective_message.reply_text(text)

async def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal() 
    return True

async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info("Function started !!!!!!!!!!!")
        """Remove the job if the user changed their mind."""
        chat_id = update.effective_message.chat_id 
        logger.info("Got ID")
        job_removed = await remove_job_if_exists(str(chat_id), context)
        logger.info("Removed job")
        ## Duplicate code
        #text = "Daily meal notifications turned off" if job_removed else "Daily meal notifications are already turned off"
        return job_removed # type: ignore
    except:
        pass
        ## Duplicate code
        ##await update.effective_message.reply_text(text)

# ~FINISHED ~ (DAILY MEAL NOTIFICATION FUNCTIONS)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    application = Application.builder().token(TOKEN).build()# type: ignore

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(dining, pattern="^" + str(DINING) + "$"),
                CallbackQueryHandler(sendDailyMenu, pattern="^" + str(SENDDAILYMENU) + "$"),
                CallbackQueryHandler(sendWeeklyMenu, pattern="^" + str(SENDWEEKLYMENU) + "$"),
                CallbackQueryHandler(onDiningNotifications, pattern="^" + str(ONDINING) + "$"),
                CallbackQueryHandler(offDiningNotifications, pattern="^" + str(OFFDINING) + "$"),
                CallbackQueryHandler(about, pattern="^" + str(ABOUT) + "$"),
                CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
                #CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
                #CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
                #CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
                #CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
                #CallbackQueryHandler(soon, pattern="^" + str(SOON) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(START) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(QUIT) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()