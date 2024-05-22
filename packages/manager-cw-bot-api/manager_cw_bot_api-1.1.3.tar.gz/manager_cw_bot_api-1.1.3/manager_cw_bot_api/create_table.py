"""
Module of the creation tables for the DB.
"""
import pymysql


class CreateTable:
    """
    Class of the creation tables for admin.
    """
    def __init__(self, connection: pymysql.connections.Connection, cursor):
        self._connection: pymysql.connections.Connection = connection
        self._cursor = cursor

    def create(self) -> None:
        """
        Create users table in MySQL.

        :return: None.
        """
        query: str = """CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        id_ticket VARCHAR(25) UNIQUE NOT NULL,
        username VARCHAR(255) NOT NULL,
        tg_id_sender VARCHAR(25) NOT NULL,
        ticket_data text NOT NULL,
        create_at VARCHAR(255) NOT NULL,
        status VARCHAR(255) NOT NULL DEFAULT "50",
        subject VARCHAR(25) NOT NULL DEFAULT "NotSubject"
        );
        """
        self._cursor.execute(query)
        self._connection.commit()

    def create_analytics(self):
        """
        Create analytics table in MySQL.

        :return: None.
        """
        query: str = """CREATE TABLE IF NOT EXISTS analytics (
        count_of_ai_queries INT NOT NULL DEFAULT 1,
        count_of_tickets_system INT NOT NULL DEFAULT 1,
        count_of_thanks_from_users INT NOT NULL DEFAULT 1
        );
        """

        self._cursor.execute(query)
        self._connection.commit()
