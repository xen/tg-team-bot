#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot that delete added/left user message from channel.
"""
import os
import sys
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep


update_id = None
TOKEN = os.environ.get('TOKEN', None)
if not TOKEN:
    print("No token provided. Run app: $ TOKEN=NNN:XXX python clean-channel.py")
    sys.exit(1)

bot = telegram.Bot(TOKEN)


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    while True:
        try:
            run(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def run(bot):
    """Based on Echo-bot from examples folder."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        msg = update.message

        if msg:  # These type of messages should be filtered.
            if (
                msg["new_chat_members"] is not None
                or msg["left_chat_member"] is not None
            ):
                logging.info(f"Delete message {msg.message_id} from chat {msg.chat.id}")
                bot.delete_message(
                    chat_id=msg.chat.id, message_id=msg.message_id,
                )


if __name__ == "__main__":
    main()
