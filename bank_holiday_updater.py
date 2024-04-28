import os
import requests
import sqlite3
import threading
import time
from dotenv import load_dotenv

load_dotenv()


class BankHolidayUpdater:
    def __init__(self, time_loop=60, database_name="bank_holidays.db", api_url=os.getenv("API_URL")):
        self.TIMELOOP = time_loop
        self.DATABASE_NAME = database_name
        self.API_URL = api_url
        self.mutex = threading.Lock()

    def fetch_data(self):
        try:
            response = requests.get(self.API_URL)
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to fetch data from API:", response.status_code)
                return None
        except Exception as e:
            print("Error fetching data:", e)
            return None

    def create_database(self, conn=None, keep_conn_open=False):
        if conn is None:
            conn = sqlite3.connect(self.DATABASE_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bank_holidays (
                     id INTEGER PRIMARY KEY,
                     division TEXT,
                     title TEXT,
                     date TEXT,
                     notes TEXT,
                     bunting INTEGER
                     )''')
        # Create indexes
        c.execute(
            "CREATE INDEX IF NOT EXISTS idx_division ON bank_holidays (division)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_title ON bank_holidays (title)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_date ON bank_holidays (date)")
        conn.commit()
        if not keep_conn_open:
            conn.close()

    def insert_data(self, division, title, date, notes, bunting):
        conn = sqlite3.connect(self.DATABASE_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM bank_holidays WHERE division=? AND title=? AND date=?",
                  (division, title, date))
        existing_entry = c.fetchone()
        if not existing_entry:
            c.execute("INSERT INTO bank_holidays (division, title, date, notes, bunting) VALUES (?, ?, ?, ?, ?)",
                      (division, title, date, notes, 1 if bunting else 0))
            conn.commit()
            print("Inserted:", title, date)
        else:
            print("Entry already exists:", title, date)
        conn.close()

    def fetch_and_cache_data(self):
        data = self.fetch_data()
        if data:
            for division, events in data.items():
                for event in events['events']:
                    self.insert_data(
                        division, event['title'], event['date'], event['notes'], event['bunting'])
            print("Data cached successfully.")

    def main(self):
        self.create_database()

        # Fetch and cache data periodically
        while True:
            with self.mutex:
                self.fetch_and_cache_data()
            # Sleep for specified time
            time.sleep(self.TIMELOOP)


if __name__ == "__main__":
    updater = BankHolidayUpdater()
    updater.main()
