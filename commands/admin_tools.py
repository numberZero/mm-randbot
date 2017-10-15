# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import os
import random
import subprocess
import sys

import config
import tokens
from utils import my_bot, my_bot_name, user_action_log
from commands import kek

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def admin_post(message):
    user_action_log(message, "has launched post tool")
    if len(message.text.split()) > 1:
        if message.text.split()[1] == "edit":
            try:
                with open(config.file_location_lastbotpost, 'r', encoding='utf-8') as file:
                    last_msg_id = int(file.read())
                my_edited_message = ' '.join(message.text.split()[2:])
                my_bot.edit_message_text(my_edited_message, config.my_chatID, last_msg_id, parse_mode="Markdown")
                user_action_log(message, "has edited message {}:\n{}\n".format(last_msg_id, my_edited_message))
            except (IOError, OSError):
                my_bot.reply_to(message, "Мне нечего редактировать.")
        else:
            my_message = ' '.join(message.text.split()[1:])
            sent_message = my_bot.send_message(config.my_chatID, my_message, parse_mode="Markdown")
            with open(config.file_location_lastbotpost, 'w', encoding='utf-8') as file_lastmsgID_write:
                file_lastmsgID_write.write(str(sent_message.message_id))
            user_action_log(message, "has posted this message:\n{}\n".format(my_message))
    else:
        my_bot.reply_to(message, "Мне нечего постить.")


def admin_clean(message):
    if len(message.text.split()) == 1:
        return
    num_str = message.text.split()[1]
    if num_str.isdigit():
        num = int(num_str)
        user_action_log(message, "has launched cleanup {} messages".format(num))
        count = 0
        for msg_id in range(message.message_id - 1, message.message_id - num, -1):
            try:
                my_bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
                count = count + 1
            except:
                pass

        user_action_log(message, "cleaned up {} messages".format(count))


def admin_prize(message):
    if len(message.text.split()) > 1 and message.text.split()[1] == tokens.my_prize:
        all_imgs = os.listdir(config.dir_location_prize)
        rand_file = random.choice(all_imgs)
        your_file = open(config.dir_location_prize + rand_file, "rb")
        if rand_file.endswith(".gif"):
            my_bot.send_document(message.chat.id, your_file, reply_to_message_id=message.message_id)
        else:
            my_bot.send_photo(message.chat.id, your_file, reply_to_message_id=message.message_id)
        your_file.close()
        user_action_log(message, "got that prize:\n{0}\n".format(your_file.name))


def kill_bot(message):
    if not hasattr(kill_bot, "check_sure"):
        kill_bot.check_sure = True
        return

    try:
        file_killed_write = open(config.bot_killed_filename, 'w', encoding='utf-8')
        file_killed_write.close()
    except RuntimeError:
        pass

    my_bot.send_document(message.chat.id, "https://t.me/mechmath/169445",
                         caption="Ухожу на отдых!", reply_to_message_id=message.message_id)
    user_action_log(message, "remotely killed bot.")
    sys.exit()


def update_bot(message):
    if not hasattr(update_bot, "check_sure"):
        update_bot.check_sure = True
        return

    try:
        file_update_write = open(config.bot_update_filename, 'w', encoding='utf-8')
        file_update_write.close()
    except RuntimeError:
        pass

    my_bot.reply_to(message, "Ух, ухожу на обновление...")
    user_action_log(message, "remotely ran update script.")
    subprocess.call('bash bot_update.sh', shell=True)


# Для админов
def admin_toys(message):
    if not hasattr(kek.my_kek, "kek_enable"):
        kek.my_kek.kek_enable = True

    command = message.text.split()[0].lower()
    if command in ["/post", "/prize", "/kek_enable", "/kek_disable", "/update_bot", "/kill", "/clean"]:
        user_action_log(message, "has launched admin tools")

    if command == "/post":
        admin_post(message)
    elif command == "/prize":
        admin_prize(message)
    elif command == "/kek_enable":
        kek.my_kek.kek_enable = True
        user_action_log(message, "enabled kek")
    elif command == "/kek_disable":
        kek.my_kek.kek_enable = False
        user_action_log(message, "disabled kek")
    elif command == "/clean":
        admin_clean(message)
    elif command == "/update":
        if message.text.split()[1] == my_bot_name:
            update_bot(message)
    elif command == "/kill":
        if message.text.split()[1] == my_bot_name:
            kill_bot(message)
