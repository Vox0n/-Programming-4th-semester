import sqlite3
from datetime import datetime


class DBManager:
    """
    Класс для работы с базой данных SQLite.
    Реализует сохранение и получение курсов валют.
    """

    def __init__(self, db_name="currency.db"):
        """Инициализация подключения к БД"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создание таблиц в БД"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code TEXT NOT NULL,
                rate REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracked_currencies (
                currency_code TEXT PRIMARY KEY
            )
        """)
        self.conn.commit()

    def save_rates(self, rates):
        """Сохранение курсов валют в БД"""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            for code, rate in rates.items():
                self.cursor.execute("""
                    INSERT INTO rates (currency_code, rate, date)
                    VALUES (:code, :rate, :date)
                """, {
                    "code": code,
                    "rate": rate,
                    "date": current_date
                })
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении в БД: {e}")
            self.conn.rollback()

    def get_latest_rates(self):
        """Получение последних курсов из БД"""
        try:
            self.cursor.execute("""
                SELECT r.currency_code, r.rate, r.date
                FROM rates r
                INNER JOIN (
                    SELECT currency_code, MAX(date) as max_date
                    FROM rates
                    GROUP BY currency_code
                ) latest ON r.currency_code = latest.currency_code 
                        AND r.date = latest.max_date
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def save_tracked_currencies(self, currencies):
        """Сохранение списка отслеживаемых валют"""
        try:
            self.cursor.execute("DELETE FROM tracked_currencies")
            for currency in currencies:
                self.cursor.execute("""
                    INSERT INTO tracked_currencies (currency_code)
                    VALUES (:code)
                """, {"code": currency})
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении валют: {e}")
            self.conn.rollback()

    def get_tracked_currencies(self):
        """Получение списка отслеживаемых валют"""
        try:
            self.cursor.execute("SELECT currency_code FROM tracked_currencies")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка при получении валют: {e}")
            return []

    def __del__(self):
        """Закрытие соединения с БД при удалении объекта"""
        self.conn.close()