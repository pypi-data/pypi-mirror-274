"""
Module of the Manager-Business-Helper Bot.
"""
import datetime
import json

import telebot
from telebot import types
import pymysql

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.create_table import CreateTable
from manager_cw_bot_api.tickets import (TicketUserView, TicketAdminView)
from manager_cw_bot_api.gigachatai import GigaChatAI
from manager_cw_bot_api.analytics import Analytic
from manager_cw_bot_api.business_handler import (BusinessHandler, Thanks, Congratulation, ProblemWithBot)
from manager_cw_bot_api.mysql_connection import Connection


class Manager(telebot.TeleBot):
    """
    Manager of the Alex's Account and helper 'AI'.
    """
    def __init__(self, bot_token: str, business_conn_id: str, admin_id: int,
                 mysql_data: dict) -> None:
        super().__init__(bot_token)
        self.__business_connection_id: str = business_conn_id
        self.__admin_id: int = admin_id
        self.__mysql_data: dict = mysql_data
        try:
            connection = pymysql.connections.Connection(
                host=mysql_data["HOST"],
                user=mysql_data["USERNAME"],
                password=mysql_data["PASSWORD"],
                database=mysql_data["DB_NAME"],
                port=mysql_data["PORT"]
            )
            cursor = connection.cursor()
            creator_mysql = CreateTable(connection, cursor)
            creator_mysql.create()
            creator_mysql.create_analytics()

        except Exception as e:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {e} | "
                           f"The error of database in __init__ of "
                           f"business.py of Manager-Class.\n")
            print(e)

    def __chat_action(self, chat_id: int | str, action: str) -> None:
        """
        Send chat action.

        :param chat_id: Chat ID.
        :param action: Action.

        :return: None.
        """
        self.send_chat_action(chat_id=chat_id, action=action, timeout=15000,
                              business_connection_id=self.__business_connection_id)

    def __messages_to_bot(self, message: types.Message) -> None:
        """
        Answers to different users include admin.

        :param message: Message of a user.
        :return: None.
        """
        if int(message.from_user.id) == self.__admin_id:
            try:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"{message.from_user.first_name}, hello! Your menu is here:",
                    reply_markup=Buttons.get_menu_admin()
                )

            except Exception as ex:
                with open("logs.txt", 'a') as logs:
                    logs.write(
                        f"{datetime.datetime.now()} | {ex} | The error in "
                        f"__messages_to_bot_if_you_are_admin of business.py.\n")
                print(f"The Error (ex-messages_to_bot_if_you_are_admin): {ex}")

        else:
            try:
                self.send_message(
                    chat_id=message.from_user.id,
                    text="Hi! I'm your helper :) Please, select the required button below",
                    reply_markup=Buttons.get_menu_user()
                )

            except Exception as ex:
                with open("logs.txt", 'a') as logs:
                    logs.write(
                        f"{datetime.datetime.now()} | {ex} | The error in "
                        f"__messages_to_bot_if_you_are_user of business.py.\n")
                print(f"The Error (ex-messages_to_bot_if_you_are_user): {ex}")

    def __answer_to_user(self, message: types.Message) -> None:
        """
        Answer to a user from admin-account (as admin).

        :param message: Message of a user.
        :return: None.
        """
        chat_id: int = message.chat.id
        action: str = "typing"

        if message.from_user.id != self.__admin_id:

            with open("bot.json", "r", encoding='utf-8') as file:
                data: dict = json.load(file)

            data = data["BUSINESS_HANDLER"]

            thanks_sticker = data["THANKS"]["THANKS_STICKER"]
            congratulation_sticker = data["CONGRATULATION"]["CONGRATULATION_STICKER"]
            problem_with_bot_sticker = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_STICKER"]

            thanks_text = data["THANKS"]["THANKS_TEXT"]
            congratulation_text = data["CONGRATULATION"]["CONGRATULATION_TEXT"]
            problem_with_bot_text = data["PROBLEM_WITH_BOT"]["PROBLEM_WITH_BOT_TEXT"]

            if "пасиб" in message.text.lower() or "thank" in message.text.lower() \
                    or "благодарю" in message.text.lower() or "спасиб" in message.text.lower():
                self.__chat_action(chat_id, action)
                try:
                    if thanks_text["MSG"] != "NONE":
                        if thanks_text["OFFSET"] != "NONE":
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=thanks_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=thanks_text["OFFSET"],
                                    length=thanks_text["LENGTH"],
                                    custom_emoji_id=thanks_text["C_E_ID"]
                                )]
                            )
                        else:
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=thanks_text["MSG"]
                            )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (THANKS_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if thanks_sticker != "NONE":
                        self.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=thanks_sticker
                        )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (THANKS_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")

            if "с днём рожден" in message.text.lower() or "happy birthday" in \
                    message.text.lower() or "с праздник" in message.text.lower() \
                    or "с др" in message.text.lower():
                self.__chat_action(chat_id, action)

                try:
                    if congratulation_text["MSG"] != "NONE":
                        if congratulation_text["OFFSET"] != "NONE":
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=congratulation_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=congratulation_text["OFFSET"],
                                    length=congratulation_text["LENGTH"],
                                    custom_emoji_id=congratulation_text["C_E_ID"]
                                )]
                            )
                        else:
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=congratulation_text["MSG"]
                            )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (CONGRATULATION_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if congratulation_sticker != "NONE":
                        self.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=congratulation_sticker
                        )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (CONGRATULATION_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")

            if ('не работает бот' in message.text.lower() or 'бот не работает' in
                    message.text.lower()):
                self.__chat_action(chat_id, action)

                try:
                    if problem_with_bot_text["MSG"] != "NONE":
                        if problem_with_bot_text["OFFSET"] != "NONE":
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=problem_with_bot_text["MSG"],
                                entities=[types.MessageEntity(
                                    type='custom_emoji',
                                    offset=problem_with_bot_text["OFFSET"],
                                    length=problem_with_bot_text["LENGTH"],
                                    custom_emoji_id=problem_with_bot_text["C_E_ID"]
                                )]
                            )
                        else:
                            self.send_message(
                                business_connection_id=self.__business_connection_id,
                                chat_id=chat_id,
                                text=problem_with_bot_text["MSG"]
                            )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (PROBLEM_WITH_BOT_TEXT) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")
                try:
                    if problem_with_bot_sticker != "NONE":
                        self.send_sticker(
                            business_connection_id=self.__business_connection_id,
                            chat_id=chat_id,
                            sticker=problem_with_bot_sticker
                        )
                except Exception as ex:
                    self.send_message(
                        chat_id=self.__admin_id,
                        text=f"Sorry! The message (PROBLEM_WITH_BOT_STICKER) can't send!\n{ex}"
                    )
                    with open("logs.txt", 'a') as logs:
                        logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                                   f"__answer_to_user-function of business.py\n")

    def __explore_show_users_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Explore to show user's ticket by id.

        :param call_query: Callback Query.
        :return: None.
        """
        self.edit_message_text(
            text=f"⚠ Please, tell me <b>ID Ticket</b>, which you want to look at.",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="HTML"
        )
        self.register_next_step_handler(call_query.message, self.__get_id_ticket_for_show)

    def __get_id_ticket_for_show(self, message: types.Message) -> None:
        """
        Get id ticket for admin answer/view or teh user view.

        :param message: Message (ID ticket) from admin/the user.
        :return: None.
        """
        connection: pymysql.connections.Connection | str = Connection.get_connection(
            self.__mysql_data
        )
        cursor = connection.cursor()

        id_ticket: str = message.text
        if len(id_ticket) == 5:
            query: str = f"""SELECT username, tg_id_sender, ticket_data, create_at, status, 
            subject FROM users WHERE id_ticket = %s;"""
            cursor.execute(query, (id_ticket,))
            result: tuple = cursor.fetchall()
            if len(result) == 0:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! Data is none!\n"
                         f"Your message: {message.text}",
                    reply_markup=Buttons.get_menu_on_back_or_main()
                )
            else:
                response: tuple = result[0]

                username: str = response[0]
                id_user_tg: int = int(response[1])
                content_ticket_data: str = response[2]
                create_at: str = response[3]
                status: str = response[4]
                subject: str = response[5]

                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"👤 Sender: @{username}\n"
                         f"#️⃣ ID Sender: {id_user_tg}\n\n"
                         f"#️⃣ ID Ticket: {id_ticket}\n"
                         f"⌚ Create at {create_at}\n"
                         f"🌐 STATUS: {status}\n"
                         f"✉ Subject: {subject}\n"
                         f"📩 Content: \n\n      {content_ticket_data}",
                    reply_markup=Buttons.get_menu_on_back_or_main()
                )

        else:
            self.send_message(
                chat_id=message.from_user.id,
                text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 symbols!\n"
                     f"Your message: {message.text}",
                reply_markup=Buttons.get_menu_on_back_or_main()
            )

        connection.close()

    def __explore_answer_users_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to user.

        :param call_query: Callback Query.
        :return: None.
        """
        if call_query.from_user.id == self.__admin_id:
            self.edit_message_text(
                text=f"⚠ Please, tell me ID Ticket, your message and new status of the ticket, "
                     f"which you want to answer. System use special "
                     f"parse-mode here!\n\n"
                     f"FORMAT your message: ``` ID_TICKET ~ MESSAGE ~ "
                     f"NEW_STATUS```\n"
                     f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                     f"it!): "
                     f"https://imgbly.com/;\n"
                     f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                     f"checked it!): https://www.file.io/;\n"
                     f"3. IF YOU WANT *TO USE THE SYMBOL*: ```'``` - *USE THIS* (backquote): ```` "
                     f"```"
                     f"4. IF YOU WANT *TO USE THE SYMBOL*: ```\\``` - *USE THIS* (double slash): "
                     f"```\\\\```"
                     f"But when you'll send, you agree with rules of "
                     f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                     f"2. Don't use TicketSystem like personal messenger!_",
                chat_id=call_query.message.chat.id,
                message_id=call_query.message.message_id,
                parse_mode="Markdown"
            )
            self.register_next_step_handler(call_query.message, self.__get_id_ticket_for_answer)

    def __get_id_ticket_for_answer(self, message: types.Message) -> None:
        """
        Get id ticket for answer to user and sending answer to the user.

        :param message: Message of the user.
        :return: None.
        """
        try:
            connection: pymysql.connections.Connection | str = Connection.get_connection(
                self.__mysql_data
            )
            cursor = connection.cursor()

            id_ticket: str = message.text.split(' ~ ')[0]
            message_for_ticket: str = message.text.split(' ~ ')[1]
            new_status: str = message.text.split(' ~ ')[2]

            if len(id_ticket) == 5:
                query: str = f"""SELECT tg_id_sender, ticket_data, subject
                             FROM users WHERE id_ticket = %s;"""
                cursor.execute(query, (id_ticket,))
                result: tuple = cursor.fetchall()
                if len(result) == 0:
                    self.reply_to(
                        message=message,
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )
                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    subject: str = response[2]

                    self.send_message(
                        chat_id=tg_id_sender,
                        text=f"👤 ADMIN ANSWER\n\n"
                             f"#️⃣ ID Ticket: {id_ticket}\n"
                             f"🌐 STATUS: {new_status}\n"
                             f"✉ Subject: {subject}\n"
                             f"📩 Content of message: \n\n      {message_for_ticket}",
                        reply_markup=Buttons.get_menu_on_back_or_main()
                    )
                    msg: types.Message = self.send_message(
                        chat_id=message.from_user.id,
                        text=f"✅ SUCCESSFUL! Your message has been delivered!"
                    )
                    if (len(content_ticket_data) + len(message_for_ticket)) <= 3800:
                        new_content_data: str = (f"{content_ticket_data}\n"
                                                 f"--Admin: {message_for_ticket}")
                    else:
                        new_content_data: str = f"{message_for_ticket}"

                    query: str = f"""UPDATE users SET ticket_data = '{new_content_data}', 
                                 status = '{new_status}' WHERE id_ticket = %s;"""
                    cursor.execute(query, (id_ticket,))
                    connection.commit()
                    self.edit_message_text(
                        chat_id=message.from_user.id,
                        message_id=msg.message_id,
                        text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                        reply_markup=Buttons.get_menu_on_back_or_main()
                    )

            else:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=Buttons.get_menu_on_back_or_main()
                )

            connection.close()

        except Exception as ex:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                           f"__get_id_ticket_for_answer-function of business.py\n")
            self.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL!",
                reply_markup=Buttons.get_menu_on_back_or_main()
            )

    def __explore_answer_admin_by_ticket(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-handler) for get id ticket for answer to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        self.edit_message_text(
            text=f"⚠ Please, tell me ID Ticket, your message and new status of the ticket, "
                 f"which you want to answer. System use special "
                 f"parse-mode here!\n\n"
                 f"FORMAT your message: ``` ID_TICKET ~ MESSAGE```\n"
                 f"1. IF YOU WANT *TO ATTACH THE PHOTO use this free website* (we checked "
                 f"it!): "
                 f"https://imgbly.com/;\n"
                 f"2. IF YOU WANT *TO ATTACH THE DOCUMENT-FILE use this free website* (we "
                 f"checked it!): https://www.file.io/;\n"
                 f"3. IF YOU WANT *TO USE THE SYMBOL*: ```'``` - *USE THIS* (backquote): ```` ```"
                 f"4. IF YOU WANT *TO USE THE SYMBOL*: ```\\``` - *USE THIS* (double slash): "
                 f"```\\\\```"
                 f"But when you'll send, you agree with rules of "
                 f"'SENDER'.\n\n_1. Please, don't send spam or other ticket as spam\n"
                 f"2. Don't use TicketSystem like personal messenger!_",
            chat_id=call_query.message.chat.id,
            message_id=call_query.message.message_id,
            parse_mode="Markdown"
        )
        self.register_next_step_handler(call_query.message,
                                        self.__get_id_ticket_for_answer_for_admin)

    def __get_id_ticket_for_answer_for_admin(self, message: types.Message) -> None:
        """
        Get id ticket for answer to user and sending answer to admin.

        :param message: Message of the user.
        :return: None.
        """
        try:
            connection: pymysql.connections.Connection | str = Connection.get_connection(
                self.__mysql_data
            )
            cursor = connection.cursor()
            id_ticket: str = message.text.split(' ~ ')[0]
            message_for_ticket: str = message.text.split(' ~ ')[1]

            if len(id_ticket) == 5:
                query: str = f"""SELECT tg_id_sender, ticket_data, status, subject
                             FROM users WHERE id_ticket = %s;"""
                cursor.execute(query, (id_ticket,))
                result: tuple = cursor.fetchall()

                if len(result) == 0:
                    self.reply_to(
                        message=message,
                        text=f"Sorry! Data is none!\n"
                             f"Your message: {message.text}"
                    )
                else:
                    response: tuple = result[0]

                    tg_id_sender: int = int(response[0])
                    content_ticket_data: str = response[1]
                    status: str = response[2]
                    subject: str = response[3]

                    if tg_id_sender == message.from_user.id:
                        self.send_message(
                            chat_id=self.__admin_id,
                            text=f"👤 USER ANSWER\n\n"
                                 f"#️⃣ ID Ticket: {id_ticket}\n"
                                 f"🌐 STATUS: {status}\n"
                                 f"✉ Subject: {subject}\n"
                                 f"📩 Content of message: \n\n      {message_for_ticket}",
                            reply_markup=Buttons.get_menu_on_back_or_main()
                        )

                        msg: types.Message = self.send_message(
                            chat_id=message.from_user.id,
                            text=f"✅ SUCCESSFUL! Your message has been delivered!"
                        )
                        if (len(content_ticket_data) + len(message_for_ticket)) <= 3800:
                            new_content_data: str = (f"{content_ticket_data}\n"
                                                     f"--User: {message_for_ticket}")
                        else:
                            new_content_data: str = f"{message_for_ticket}"

                        query: str = f"""
                                     UPDATE users SET ticket_data = '{new_content_data}' 
                                     WHERE id_ticket = %s;
                                     """
                        cursor.execute(query, (id_ticket,))
                        connection.commit()
                        self.edit_message_text(
                            chat_id=message.from_user.id,
                            message_id=msg.message_id,
                            text=f"✅ SUCCESSFUL! Updated DB-data for ID: {id_ticket}!",
                            reply_markup=Buttons.get_menu_on_back_or_main()
                        )
                    else:
                        self.send_message(
                            chat_id=tg_id_sender,
                            text=f"🚫 ERROR 43! {message.from_user.first_name}, forbidden!",
                            parse_mode="Markdown",
                            reply_markup=Buttons.get_menu_on_back_or_main()
                        )

            else:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f"Sorry! It's not ID Ticket, because length of your message isn't 5 "
                         f"symbols!\nYour message: {message.text}",
                    reply_markup=Buttons.get_menu_on_back_or_main()
                )

            connection.close()

        except Exception as ex:
            with open("logs.txt", 'a') as logs:
                logs.write(f"{datetime.datetime.now()} | {ex} | The error in "
                           f"__get_id_ticket_for_answer-function of business.py\n")
            self.send_message(
                chat_id=message.from_user.id,
                text=f"❌ FAIL! {ex}",
                reply_markup=Buttons.get_menu_on_back_or_main()
            )

    def back_in_main_menu(self, call_query: types.CallbackQuery) -> None:
        """
        Back-function (to main menu).

        :param call_query: CallbackQuery.
        :return: None.
        """
        if int(call_query.from_user.id) == self.__admin_id:
            try:
                self.edit_message_text(
                    text=f"{call_query.from_user.first_name}, you're in main menu!",
                    chat_id=call_query.from_user.id,
                    message_id=call_query.message.message_id,
                    reply_markup=Buttons.get_menu_admin()
                )

            except Exception as ex:
                with open("logs.txt", 'a') as logs:
                    logs.write(
                        f"{datetime.datetime.now()} | The error in "
                        f"__back_in_main_menu_if_admin-function of gigachatai.py.\n")
                print(f"The Error (ex): {ex}")

        else:
            try:
                self.edit_message_text(
                    text=f"{call_query.from_user.first_name}, you're in main menu!",
                    chat_id=call_query.from_user.id,
                    message_id=call_query.message.message_id,
                    reply_markup=Buttons.get_menu_user()
                )

            except Exception as ex:
                with open("logs.txt", 'a') as logs:
                    logs.write(
                        f"{datetime.datetime.now()} | The error in "
                        f"__back_in_main_menu_if_user-function of business.py.\n")
                print(f"The Error (ex): {ex}")

    def __ai_assistance(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for go to the AI-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        giga_chat_ai_helper: GigaChatAI = (
            GigaChatAI(
                self, call_query,
                self.__mysql_data,
                self.__admin_id
            )
        )
        giga_chat_ai_helper.show_info_edit_text()
        self.register_next_step_handler(call_query.message, giga_chat_ai_helper.request)

    def __user_menu_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for go to the Tickets-Menu.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket: TicketUserView = TicketUserView(
            self,
            self.__mysql_data
        )
        ticket.show_user_menu(call_query)

    def __admin_menu_tickets(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (callback-handler) for show tickets to admin.

        :param call_query: Callback Query.
        :return: None.
        """
        ticket: TicketAdminView = TicketAdminView(
            self,
            self.__mysql_data
        )
        ticket.show_admin_users_tickets(call_query)

    def __analytic_data(self, call_query: types.CallbackQuery) -> None:
        """
        Handler of the analytic-menu (UI) for admin.

        :param call_query: Callback Query.
        :return: None.
        """
        analytic: Analytic = Analytic(
            self,
            self.__mysql_data,
            call_query
        )
        analytic.analyse()

    def __business_handler(self, call_query: types.CallbackQuery) -> None:
        """
        Handler (call-query) for admin (with business) - start main handler.

        :param call_query: Callback Query.
        :return: None.
        """
        handler: BusinessHandler = BusinessHandler(
            self, call_query
        )
        handler.run()

    def run(self) -> None:
        """
        Run-function Bot.
        """
        self.register_business_message_handler(
            callback=self.__answer_to_user
        )

        self.register_message_handler(
            callback=self.__messages_to_bot,
            content_types=["text"]
        )

        self.register_callback_query_handler(
            callback=self.__ai_assistance,
            func=lambda call: call.data == "ai_assistance_request"
        )
        self.register_callback_query_handler(
            callback=self.__user_menu_tickets,
            func=lambda call: call.data == "explore_user_tickets_menu"
        )
        self.register_callback_query_handler(
            callback=self.__admin_menu_tickets,
            func=lambda call: call.data == "explore_admin_show_tickets_menu"
        )
        self.register_callback_query_handler(
            callback=self.__explore_answer_users_ticket,
            func=lambda call: call.data == "explore_answer_to_user"
        )
        self.register_callback_query_handler(
            callback=self.__explore_answer_admin_by_ticket,
            func=lambda call: call.data == "explore_answer_to_admin"
        )
        self.register_callback_query_handler(
            callback=self.__explore_show_users_ticket,
            func=lambda call: call.data == "explore_show_ticket_by_id"
        )
        self.register_callback_query_handler(
            callback=self.__explore_show_users_ticket,
            func=lambda call: call.data == "explore_show_ticket_by_id"
        )
        self.register_callback_query_handler(
            callback=self.__analytic_data,
            func=lambda call: call.data == "analytic_data"
        )
        self.register_callback_query_handler(
            callback=self.__business_handler,
            func=lambda call: call.data == "business_handler"
        )
        self.register_callback_query_handler(
            callback=self.back_in_main_menu,
            func=lambda call: call.data == "back_in_main_menu"
        )

        self.polling(
            non_stop=True,
            interval=0
        )


def get_data(file_path="bot.json") -> dict:
    """
    Get data of the Alex's Manager Bot.

    :param file_path: File Path of JSON-API-keys for Bot.

    :return: Dict with data.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        data: dict = json.load(file)

        dct = dict()
        dct["BOT_TOKEN"] = data["BOT_TOKEN"]
        dct["business_connection_id"] = data["business_connection"]["id"]
        dct["business_connection_is_enabled"] = data["business_connection"]["is_enabled"]
        dct["ADMIN"] = data["business_connection"]["user"]["id"]

        dct["MYSQL"] = data["MYSQL"]

        dct["BUSINESS_HANDLER"] = data["BUSINESS_HANDLER"]

        return dct


def run() -> None:
    """
    Run Function of the main-file.

    :return: None.
    """
    try:
        data: dict = get_data()
        if data["business_connection_is_enabled"] == "True":
            bot: Manager = Manager(data["BOT_TOKEN"], data["business_connection_id"],
                                   data["ADMIN"], data["MYSQL"])
            bot.run()

        else:
            print("Business Connection isn't enabled!")
    except Exception as ex:
        with open("logs.txt", 'a') as logs:
            logs.write(f"\n{datetime.datetime.now()} | {ex} | The error in run-function of "
                       f"business.py.\n")
        print(f"The Error (ex-run-func): {ex}")
