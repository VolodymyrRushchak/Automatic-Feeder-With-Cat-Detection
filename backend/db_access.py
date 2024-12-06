import datetime

import pandas as pd
import mysql.connector


class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="30122003VG",
            database="cat_tracker"
        )
        self.cursor = self.db.cursor()
        self.write_query = "INSERT INTO camera_history (time_point, cat_present) VALUES (NOW(), %s)"
        self.get_all_query = "SELECT * FROM camera_history"
        self.get_cat_ratio_query = "SELECT avg(cat_present) FROM camera_history"
        self.get_filming_time_query = "SELECT timediff(max(time_point), min(time_point)) FROM camera_history"
        self.get_time_from_last_cat_query = \
            "SELECT timediff(NOW(), max(time_point)) FROM camera_history WHERE cat_present = 1"
        self.get_user_query = 'SELECT * FROM users WHERE email = %s AND password = %s'
        self.is_account_query = 'SELECT * FROM users WHERE email = %s'
        self.add_account_query = "INSERT INTO users VALUES (NULL, %s, %s, %s, 'user')"

    def write(self, cat_present: bool) -> None:
        self.cursor.execute(self.write_query, (cat_present,))
        self.db.commit()

    def get_all(self) -> pd.DataFrame:
        self.cursor.execute(self.get_all_query)
        data = self.cursor.fetchall()
        self.db.commit()
        return pd.DataFrame(data, columns=['id', 'time_point', 'cat_present'])

    def get_cat_ratio(self) -> float:
        self.cursor.execute(self.get_cat_ratio_query)
        data = self.cursor.fetchall()
        self.db.commit()
        return data[0][0]

    def get_filming_time(self) -> datetime.timedelta:
        self.cursor.execute(self.get_filming_time_query)
        data = self.cursor.fetchall()
        self.db.commit()
        return data[0][0]

    def get_time_from_last_cat(self) -> datetime.timedelta:
        self.cursor.execute(self.get_time_from_last_cat_query)
        data = self.cursor.fetchall()
        self.db.commit()
        return data[0][0]

    def get_user(self, email: str, password: str) -> dict:
        self.cursor.execute(self.get_user_query, (email, password))
        user = self.cursor.fetchone()
        self.db.commit()
        if user:
            return {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3], 'privilege': user[4]}
        return {}

    def is_account(self, email: str) -> bool:
        self.cursor.execute(self.is_account_query, (email,))
        account = self.cursor.fetchone()
        self.db.commit()
        return bool(account)

    def add_account(self, user_name: str, email: str, password: str) -> None:
        self.cursor.execute(self.add_account_query, (user_name, email, password))
        self.db.commit()
