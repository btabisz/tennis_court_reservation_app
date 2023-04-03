from datetime import timedelta, datetime
from reservations import Reservations
from user_inputs import UserInputsApp
from validations import Validations


class PrintApp:
    def __init__(self):
        self.reservations = Reservations()
        self.validations = Validations()
        self.inputs = UserInputsApp()

    def start_print_app(self):
        print('Print schedule')
        while True:
            print_start_date = self.inputs.get_date("start")
            if print_start_date == 1:
                break
            print_end_date = self.inputs.get_date("end")
            if print_end_date == 1:
                break
            if print_start_date > print_end_date:
                print('You have entered wrong dates.')
                continue
            self.printer(print_start_date, print_end_date)
            break

    @staticmethod
    def print_date(print_date):
        if print_date.date() == datetime.today().date():
            print('\nToday:')
        elif print_date.date() == datetime.today().date() + timedelta(days=1):
            print('\nTomorrow:')
        elif print_date.date() == datetime.today().date() - timedelta(days=1):
            print('\nYesterday:')
        else:
            print(f"\n{print_date.strftime('%A, %d. %B %Y')}:")

    def printer(self, print_start_date, print_end_date):
        print_date = print_start_date
        conn = self.reservations.create_connection_db()
        cur = conn.cursor()
        while print_date.date() <= print_end_date.date():
            cur.execute("SELECT name, time(start_time), time(end_time) FROM reservations WHERE date(start_time)=?"
                        "ORDER BY start_time", (print_date.date(),))
            rows = cur.fetchall()
            self.print_date(print_date)
            if len(rows) != 0:
                for row in rows:
                    print(f"* {row[0]} {row[1][0:5]} - {row[2][0:5]}")
            else:
                print('No Reservations')
            print_date += timedelta(days=1)
        conn.close()
        print("-------------------------")
