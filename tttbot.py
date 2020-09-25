import os
import smtplib
from threading import Thread

from db import Dbase
from mail import Emaill
from openapi_client.models import chat_type
from jjira import ForJira
#from TamTamBot import CallbackButtonCmd, UpdateCmn
from TamTamBot.TamTamBot import TamTamBot
from TamTamBot.utils.lng import set_use_django
from openapi_client import NewMessageBody, BotCommand, ChatType, UserAddedToChatUpdate
import logging
import time

import numpy as np



class BotDevHelper(TamTamBot):
    auth_chat_id = int(-72032408415065)
    passwords = {}


    @property
    def token(self):
        return os.environ.get('TT_BOT_API_TOKEN')

    @property
    def description(self):
        return 'Этот бот чему то / кому то помогает.\n\n' \
               'This bot something / someone helps.'

    @property
    def about(self):
        return 'Этот бот чему то / кому то помогает.'

    @staticmethod
    def authorized_user(user):
        # type: (User) -> bool
        db = Dbase('localhost', 'table_name', 'login', 'pass')
        #db.check(str(user.user_id)) == True:

        return db.check(user.user_id)

    def handle_user_added_to_chat_update(self, update):
        # type: (UserAddedToChatUpdate) -> bool
        # Здесь проверяем что пользователь авторизован - если нет, выкидываем его
        if update.chat_id == BotDevHelper.auth_chat_id:
            if not self.authorized_user(update.user):
                self.chats.remove_member(update.chat_id, update.user.user_id)
        return True

    def get_commands(self):
        # type: () -> [BotCommand]
        commands = [
            BotCommand('send_mail', 'отправить адрес для авторизации'),
            BotCommand('auth_code', 'предоставить код авторизации'),
        ]
        return commands

    def cmd_handler_send_mail(self, update):
        # type: (UpdateCmn) -> bool
        if not (update.chat_type in [ChatType.DIALOG]):
            return False
        if self.authorized_user(update.user):
            self.msg.send_message(NewMessageBody('Вы уже являетесь авторизованным пользователем!'), user_id=update.user_id)
            return True

        res = None
        if not update.this_cmd_response:  # Это прямой вызов команды, а не текстовый ответ на команду
            if update.cmd_args:  # Если вместе с командой сразу переданы аргументы
                email_addr = None
                parts = update.cmd_args.get('c_parts') or []
                if parts:
                    for line in parts:
                        for part in line:
                            email_addr = str(part)

                if email_addr:
                    res = self.send_pass_code(update, email_addr)
            else:  # Вывод запроса для ожидания ответа
                self.msg.send_message(NewMessageBody('Введите адрес почты:'), user_id=update.user_id)
                update.required_cmd_response = True  # Сообщаем о необходимости ожидания текстового ответа
        else:  # Текстовый ответ команде
            email_addr = update.message.body.text

            res = self.send_pass_code(update, email_addr)

        return bool(res)

    def cmd_handler_auth_code(self, update):
        # type: (UpdateCmn) -> bool
        if not (update.chat_type in [ChatType.DIALOG]):
            return False
        if self.authorized_user(update.user):
            self.msg.send_message(NewMessageBody('Вы уже являетесь авторизованным пользователем!'), user_id=update.user_id)
            return True

        res = None
        if not update.this_cmd_response:  # Это прямой вызов команды, а не текстовый ответ на команду
            if update.cmd_args:  # Если вместе с командой сразу переданы аргументы
                auth_code = None
                parts = update.cmd_args.get('c_parts') or []
                if parts:
                    for line in parts:
                        for part in line:
                            auth_code = str(part)

                if auth_code:
                    res = self.process_pass_code(update, auth_code)
            else:  # Вывод запроса для ожидания ответа
                self.msg.send_message(NewMessageBody('Введите код, полученный в письме:'), user_id=update.user_id)
                update.required_cmd_response = True  # Сообщаем о необходимости ожидания текстового ответа
        else:  # Текстовый ответ команде
            auth_code = update.message.body.text
            res = self.process_pass_code(update, auth_code)

        return bool(res)

    def send_pass_code(self, update, email_addr):
        # type: (UpdateCmn, str) -> bool

        bot_mail = Emaill('mail', 'pass')
        BotDevHelper.passwords[update.user_id] = bot_mail.passw()
        q = bot_mail.reg(email_addr, BotDevHelper.passwords[update.user_id])
        self.msg.send_message(NewMessageBody(f'{q}'),
                                      user_id=update.user_id)
        return q == 'Message is sent'


    def process_pass_code(self, update, auth_code):
        # type: (UpdateCmn, str) -> bool

        if self.authorized_user(update.user):
            self.msg.send_message(NewMessageBody('Вы уже являетесь авторизованным пользователем!'), user_id=update.user_id)
            return True
        if auth_code == BotDevHelper.passwords.get(update.user_id):
            self.msg.send_message(NewMessageBody('Поздравляем, авторизация успешна!'), user_id=update.user_id)
            db = Dbase('localhost', 'table_name', 'login', 'pass')
            db.insert(str(update.user_id))
            return True
        else:
            self.msg.send_message(NewMessageBody('Введён неверный код. Повторите.'), user_id=update.user_id)
            return False

    def process_jira_res(self):
        x = ForJira(['filter=77863', 'filter=78775', 'filter=78776', 'filter=78774', 'filter=77295'], 'login', 'Pass')
        auth = x.authorization()
        first = x.oneResult(auth)
        newArr = []
        #print(first)
        self.msg.send_message(NewMessageBody(first), chat_id=BotDevHelper.auth_chat_id)

        while (1):
            m = x.getResult(first, newArr, auth)
            if m[0] != 0:
                for i in range(np.size(m[0])):
                    self.msg.send_message(NewMessageBody(str(m[0][i])), chat_id=BotDevHelper.auth_chat_id)
            first = m[2]
            newArr = []
            time.sleep(60)
        pass

if __name__ == '__main__':
    set_use_django(False)
    #
    tt_bot = BotDevHelper()
    tt_bot.polling_sleep_time = 0

    t = Thread(target=tt_bot.polling, args=())
    t.start()

    tt_bot.process_jira_res()
    BotDevHelper().polling()