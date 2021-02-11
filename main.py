from decouple import config
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from bot.callback import callback
from bot.commands import start
from entities.game import Game
from bot.inline import inline
from entities.user import MyUser


def load_data():
    MyUser.load_all()
    Game.load_all()


if __name__ == '__main__':
    load_data()

    updater = Updater(config('BOT_TOKEN'))
    dp = updater.dispatcher

    handlers = [
        CommandHandler('start', start),
        InlineQueryHandler(inline),
        CallbackQueryHandler(callback)
    ]

    for h in handlers:
        dp.add_handler(h)

    updater.start_polling()
    updater.idle()
