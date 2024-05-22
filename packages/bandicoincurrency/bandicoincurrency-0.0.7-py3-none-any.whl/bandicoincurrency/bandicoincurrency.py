import json
import mysql.connector
from datetime import datetime

# Configure your MySQL connection parameters
db_config = {
    'user': 'u594_3CAYzXhRhD',
    'password': '3^1QsKcyZTD0OaRd+9qr1V!n',
    'host': 'berry.sillydev.co.uk',
    'port': 3306,
    'database': 's594_domain_data'
}


class BandicoinCurrency:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect_to_db(self):
        return mysql.connector.connect(**self.db_config)

    def initialize_database(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            currency INT DEFAULT 150,
            last_claim_date DATE
        )
        """)
        conn.commit()

        # Check if the database is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        if result[0] == 0:
            self.load_data_from_json(cursor)

        cursor.close()
        conn.close()

    def load_data_from_json(self, cursor):
        try:
            with open("bandicoin_data.json", "r") as file:
                database = json.load(file)

            for user, data in database.items():
                currency = data.get("currency", 150)
                last_claim_date = data.get("last_claim_date", None)
                if last_claim_date:
                    last_claim_date = datetime.strptime(
                        last_claim_date, "%m/%d/%Y").date()
                cursor.execute(
                    "INSERT INTO users (username, currency, last_claim_date) VALUES (%s, %s, %s)",
                    (user, currency, last_claim_date)
                )
        except FileNotFoundError:
            print("bandicoin_data.json not found. Starting with an empty database.")

    def give_currency(self, receiver, amount: int, sender):
        conn = self.connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT currency FROM users WHERE username = %s", (sender,))
        sender_currency = cursor.fetchone()
        if not sender_currency:
            cursor.close()
            conn.close()
            raise ValueError(f"User '{sender}' not found")

        cursor.execute(
            "SELECT currency FROM users WHERE username = %s", (receiver,))
        receiver_currency = cursor.fetchone()
        if not receiver_currency:
            cursor.close()
            conn.close()
            raise ValueError(f"User '{receiver}' not found")

        if sender_currency[0] < amount:
            cursor.close()
            conn.close()
            raise ValueError("Insufficient currency")

        cursor.execute(
            "UPDATE users SET currency = currency - %s WHERE username = %s", (amount, sender))
        cursor.execute(
            "UPDATE users SET currency = currency + %s WHERE username = %s", (amount, receiver))
        conn.commit()
        cursor.close()
        conn.close()

        return f"{amount} currency given from {sender} to {receiver}"

    def claim_daily(self, user):
        conn = self.connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT currency, last_claim_date FROM users WHERE username = %s", (user,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            conn.close()
            return None

        current_time = datetime.now()
        last_claim_date = result[1]

        if not last_claim_date or current_time.date() != last_claim_date:
            cursor.execute("UPDATE users SET currency = currency + 15, last_claim_date = %s WHERE username = %s",
                           (current_time.date(), user))
            conn.commit()
            cursor.close()
            conn.close()
            return "Claimed daily currency!"

        cursor.close()
        conn.close()
        return "Come back tomorrow, please."

    def currency_balance(self, user):
        conn = self.connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT currency FROM users WHERE username = %s", (user,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            return "User not found"

        return result[0]

    def register_user(self, user):
        conn = self.connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username FROM users WHERE username = %s", (user,))
        result = cursor.fetchone()

        if not result:
            current_time = datetime.now()
            cursor.execute("INSERT INTO users (username, currency, last_claim_date) VALUES (%s, %s, %s)",
                           (user, 150, current_time.date()))
            conn.commit()
            cursor.close()
            conn.close()
            return f"User '{user}' registered successfully"

        cursor.close()
        conn.close()
        return None


bandicoin = BandicoinCurrency(db_config)
bandicoin.initialize_database()
