"""
Module of the create button for the menu and Bot in general.
"""
from telebot import types


class Buttons:
    """
    Class for get the buttons in chats.
    """
    @staticmethod
    def get_email() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the help.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        btn1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="👆 Перейти", url="t.me/aleksandr_work")
        markup.add(btn1)
        return markup

    @staticmethod
    def get_var_giga_version() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the choose version of the GigaChatAI
        for the user.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        v1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💡 GigaChatLight", callback_data="gigachat_version_light"
        )
        v2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="⚡ GigaChatPRO", callback_data="gigachat_version_pro"
        )
        v3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )
        markup.row(v1).row(v2).row(v3)
        return markup

    @staticmethod
    def get_menu_user() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for the user.

        :return: Markup-button.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI Assistance", callback_data="ai_assistance_request"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❔ Help | CWR.SU", url="https://cwr.su/"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="❓ Help | Tickets SYSTEM", callback_data="explore_user_tickets_menu"
        )
        markup.row(var1).row(var2).row(var3)
        return markup

    @staticmethod
    def get_menu_user_tickets() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for the user in "TICKETS".

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💬 Show My tickets", callback_data="show_user_tickets"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💭 Send a new ticket", callback_data="send_new_ticket"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✉ Show the ticket by ID", callback_data="explore_show_ticket_by_id"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the admin", callback_data="explore_answer_to_admin"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )
        markup.row(var1).row(var2).row(var3).row(var4).row(var5)
        return markup

    @staticmethod
    def get_menu_user_tickets_again() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot AGAIN-Menu
        for the user in "TICKETS".

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Tickets Menu", callback_data="explore_user_tickets_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💭 Send a new ticket", callback_data="send_new_ticket"
        )
        markup.row(var1).row(var2)
        return markup

    @staticmethod
    def get_user_tickets(username, cursor) -> tuple:
        """
        Markup-button (Inline) of the Bot
        for the user's history of "TICKETS".

        :param username: User's name -- username.
        :param cursor: Cursor of the connection to DB by MySQL.

        :return: Tuple with data.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        query: str = f"SELECT id_ticket, create_at, subject FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result: tuple = cursor.fetchall()
        response: str = ""
        if len(result) > 0:
            for i in range(len(list(result))):
                response += (f"<b>{i + 1}</b>. ID_TCK: <code>{result[i][0]}</code>| "
                             f"CREATE_AT: {result[i][1]}| "
                             f"Subject: <blockquote>'{result[i][2]}'</blockquote>\n")
        else:
            btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="not_found"
            )
            markup.row(btn)

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Tickets Menu", callback_data="explore_user_tickets_menu"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the admin", callback_data="explore_answer_to_admin"
        )
        markup.row(var1).row(var2)

        results: tuple = (response, markup)
        return results

    @staticmethod
    def get_menu_admin() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for admin.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧠 AI Assistance", callback_data="ai_assistance_request"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📨 Show tickets", callback_data="explore_admin_show_tickets_menu"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="✉ Show the ticket by ID", callback_data="explore_show_ticket_by_id"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🗣 Answer to the user", callback_data="explore_answer_to_user"
        )
        var5: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="📈 Analytic", callback_data="analytic_data"
        )
        var6: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🧑‍💼 Business Handler", callback_data="business_handler"
        )
        markup.row(var1).row(var2).row(var3).row(var4).row(var5).row(var6)
        return markup

    @staticmethod
    def get_users_tickets_for_admin(cursor) -> tuple:
        """
        Markup-button (Inline) of the Bot
        for the admin history of "TICKETS" of the users.

        :param cursor: Cursor of the connection to DB by MySQL.
        :return: tuple of the tickets and Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        query: str = "SELECT id_ticket, username, create_at, subject FROM users"
        cursor.execute(query)
        result: tuple = cursor.fetchall()
        response: str = ""

        if len(result) > 0:
            for i in range(len(list(result))):
                response += (f"<b>{i+1}</b>. Sender: "
                             f"@{result[i][1]}| ID_TCK: <code>{result[i][0]}</code>| CREATE_AT: "
                             f"{result[i][2]}| Subject: "
                             f"<blockquote>'{result[i][3]}'</blockquote>\n")
        else:
            btn: types.InlineKeyboardButton = types.InlineKeyboardButton(
                text=f"Not Found", callback_data="not_found"
            )
            markup.row(btn)

        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )
        markup.row(var)

        results: tuple = (response, markup)
        return results

    @staticmethod
    def get_menu_business_handler() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Thanks", callback_data="handler_thanks_from_users"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Congratulation 🎉", callback_data="handler_congratulation_from_users"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🤖 Problem with bot", callback_data="handler_problem_with_bot_from_users"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_thanks() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - ThanksCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💌 Only text", callback_data="only_text_for_thanks_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker 💗", callback_data="only_sticker_for_thanks_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💞 Both: Message and sticker", callback_data="message_and_sticker_for_thanks_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_congratulation() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - CongratulationCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🎉 Only text", callback_data="only_text_for_congratulation_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker 💗", callback_data="only_sticker_for_congratulation_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Both: Message and sticker",
            callback_data="message_and_sticker_for_congratulation_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_business_handler_problem_with_bot() -> types.InlineKeyboardMarkup:
        """
        Get menu of business handler - ProblemWithBotCommandAnswer.

        :return: Markup Buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

        var1: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💬 Only text", callback_data="only_text_for_problem_with_bot_hdl"
        )
        var2: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Only Sticker ♨", callback_data="only_sticker_for_problem_with_bot_hdl"
        )
        var3: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="💫 Both: Message and sticker",
            callback_data="message_and_sticker_for_problem_with_bot_hdl"
        )
        var4: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )

        markup.row(var1).row(var2).row(var3).row(var4)

        return markup

    @staticmethod
    def get_menu_on_back_or_main() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Menu
        for admin/user that to back to the Main Menu.

        :return: Markup-buttons.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="🔙 Main Menu", callback_data="back_in_main_menu"
        )
        markup.row(var)
        return markup

    @staticmethod
    def say_thanks() -> types.InlineKeyboardMarkup:
        """
        Markup-button (Inline) of the Bot Thanks.

        :return: Markup-button.
        """
        markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        var: types.InlineKeyboardButton = types.InlineKeyboardButton(
            text="Say: Thank you! 💖", callback_data="say_thanks"
        )
        markup.row(var)
        return markup
