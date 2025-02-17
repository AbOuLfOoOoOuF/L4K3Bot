# from AstrakoBot
import os
from datetime import datetime
from typing import List
from gtts import gTTS
from telegram import Update, ChatAction, ParseMode

from tg_bot.modules.sql.clear_cmd_sql import get_clearcmd
from tg_bot import dispatcher, spamcheck
from telegram.ext import CallbackContext
from tg_bot.modules.helper_funcs.misc import delete
from tg_bot.modules.helper_funcs.decorators import kigcmd

@kigcmd(command='tts')
@spamcheck
def tts(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    delmsg = ""

    if message.reply_to_message:
        delmsg = message.reply_to_message.text

    if args:
        delmsg = "  ".join(args).lower()

        current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
        filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "ml"
        tts = gTTS(delmsg, lang)
        tts.save("k.mp3")
        with open("k.mp3", "rb") as f:
            linelist = list(f)
            linecount = len(linelist)
        if linecount == 1:
            update.message.chat.send_action(ChatAction.RECORD_AUDIO)
            lang = "en"
            tts = gTTS(delmsg, lang)
            tts.save("k.mp3")
        with open("k.mp3", "rb") as speech:
            delmsg = update.message.reply_voice(speech, quote=False)

        os.remove("k.mp3")

    else:
        delmsg = message.reply_text(
        "Reply a message or give something like:\n`/tts <message>`",
        parse_mode = ParseMode.MARKDOWN
        )

    cleartime = get_clearcmd(chat.id, "tts")

    if cleartime:
        context.dispatcher.run_async(delete, delmsg, cleartime.time)


