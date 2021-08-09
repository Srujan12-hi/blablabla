#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
from bot import LOG_CHAN
db = Database()

chan = "https://t.me/Ee_Movies"

caption = """Join Our Channel for Latest Movies \n\nhttps://t.me/joinchat/OaTbzqxxr0thNGY9"""

mv_buttons =[[
        InlineKeyboardButton('Join Our Channel ', url=chan)
    ],[
        InlineKeyboardButton('Share & Support Us', url='http://t.me/share/url?url=Join%2@Ee_Movies%20For%20Any%20Language%20Movies')
    ]]

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    usr_id, user_name, user_mention = " ", " ", " "
    usr_id, user_name, user_mention = update.from_user.id, update.from_user.username, update.from_user.mention
 
    log_msgg = f"#Request \nThis file was requested by {usr_id}\n{user_mention}\n @{user_name}"

    if file_uid:
        file_id, file_name, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        if file_type == "document":
        
            docc = await bot.send_document(
                chat_id=update.chat.id,
                document = file_id,
                caption = caption,
                parse_mode="markdown",
                reply_to_message_id=update.message_id,
                reply_markup=InlineKeyboardMarkup(mv_buttons)
            )
            forward_msg = await docc.forward(LOG_CHAN)
            await forward_msg.reply_text(log_msgg,quote=True)

        elif file_type == "video":
        
            docc = await update.reply_video(
                file_id,
                caption = caption,
                parse_mode="markdown",
                quote=True,
                reply_markup=InlineKeyboardMarkup(mv_buttons)
            )
            forward_msg = await docc.forward(LOG_CHAN)
            await forward_msg.reply_text(log_msgg,quote=True)

        elif file_type == "audio":
        
            docc = await update.reply_audio(
                file_id,
                caption = caption,
                parse_mode="markdown",
                quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'Join', url=chan
                                )
                        ]
                    ]
                )
            )
            forward_msg = await docc.forward(LOG_CHAN)
            await forward_msg.reply_text(log_msgg,quote=True)

        else:
            print(file_type)
        
        return

    buttons = [[
        InlineKeyboardButton("My Father 👨‍✈️", url="https://t.me/Ee_movies"),
        InlineKeyboardButton("Help 💡", callback_data="help")
    ],[
        InlineKeyboardButton("About 📕", callback_data="about")
    ],[ InlineKeyboardButton("Source Code ?" , callback_data="source_code")]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        reply_markup=reply_markup,
        parse_mode="html", 
        disable_web_page_preview=True
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home 🏕', callback_data='start'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ],[ 
        InlineKeyboardButton('Support Group' , url="https://t.me/joinchat/V3MKrO4yndKapy5K")]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html", 
        disable_web_page_preview=True
    )
