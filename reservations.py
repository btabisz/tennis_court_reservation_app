from datetime import timedelta
import sqlite3
from sqlite3 import Error
from validations import Validations


class Reservations:

    def __init__(self):
        self.validations = Validations()

    @staticmethod
    def create_connection_db():
        connection = None
        try:
            connection = sqlite3.connect('./db.sqlite')
        except Error as e:
            print(e)
        return connection

    def new_reservation(self, name, start_time, end_time):
        conn = self.create_connection_db()
        c = conn.cursor()
        c.execute("""INSERT INTO reservations(name, start_time, end_time) VALUES
                    (?,?,?)""", (name, start_time, end_time))
        conn.commit()
        conn.close()
        print('Congratulations, court has been booked!')
        return 0

    def check_court_availability(self, entered_datetime):
        conn = self.create_connection_db()
        cur = conn.cursor()
        cur.execute("SELECT start_time, end_time FROM reservations WHERE date(start_time)=?",
                    (entered_datetime.date(),))
        rows = cur.fetchall()
        conn.close()
        for item in rows:
            if self.validations.db_datetime_to_datetime(item[0]) <= entered_datetime < \
                    self.validations.db_datetime_to_datetime(item[1]):
                return 1
        return 0

    def get_nearest_date(self, entered_datetime):
        nearest_date = entered_datetime + timedelta(seconds=1800)
        nearest_date_back = entered_datetime - timedelta(seconds=1800)
        while True:
            if self.check_court_availability(nearest_date) == 0:
                return nearest_date
            nearest_date += timedelta(seconds=1800)
            if self.check_court_availability(nearest_date_back) == 0:
                return nearest_date_back
            if self.validations.actual_time_validation(nearest_date_back - timedelta(seconds=1800)):
                nearest_date_back -= timedelta(seconds=1800)

    def possible_book_period(self, entered_datetime):
        if self.check_court_availability(entered_datetime + timedelta(seconds=1750)) == 0:
            if self.check_court_availability(entered_datetime + timedelta(seconds=3550)) == 0:
                if self.check_court_availability(entered_datetime + timedelta(seconds=5350)) == 0:
                    return 90
                return 60
            return 30

    def user_reservations_in_week(self, name, entered_datetime):
        number_of_entered_week = entered_datetime.isocalendar()[1]
        conn = self.create_connection_db()
        cur = conn.cursor()
        cur.execute("SELECT date(start_time) FROM reservations WHERE name=? ORDER BY start_time", (name,))
        rows = cur.fetchall()
        conn.close()
        counter = 0
        for item in rows:
            if self.validations.db_date_to_date(item[0]).isocalendar()[1] == number_of_entered_week:
                counter += 1
        if counter > 2:
            return 1
        return 0

    def cancel_reservation(self, name, entered_datetime):
        conn = self.create_connection_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reservations WHERE name=? and start_time=?", (name, entered_datetime))
        if cur.fetchone():
            cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", (name, entered_datetime))
            conn.commit()
            print('Your booking has been cancelled.')
            conn.close()
            return 0
        else:
            conn.close()
            return 1
