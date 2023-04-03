from datetime import timedelta
from reservations import Reservations
from user_inputs import UserInputsApp
from validations import Validations


class ReservationApp:
    def __init__(self):
        self.reservations = Reservations()
        self.validations = Validations()
        self.inputs = UserInputsApp()

    def start_reservation_app(self):
        print('Make a reservation')
        while True:
            name = self.inputs.get_name()
            if name == 1:
                break
            while True:
                entered_datetime = self.inputs.get_start_datetime("book")
                if entered_datetime == 1:
                    break
                if self.validations.actual_time_validation(entered_datetime) == 1:
                    print('Error, booking not possible if it is less than an hour before the start time!')
                    break
                if self.check_user_reservations_in_week(name, entered_datetime) == 1:
                    break
                if self.reservations.check_court_availability(entered_datetime) == 0:
                    duration = self.reservations.possible_book_period(entered_datetime)
                    if self.make_reservation(name, entered_datetime, duration) == 2:
                        continue
                    return 0
                else:
                    nearest_date = self.reservations.get_nearest_date(entered_datetime)
                    alternative_date_answer = input(
                        f'The time you chose is unavailable, would you like to make a reservation for'
                        f' {nearest_date.strftime("%H:%M (%d.%m.%Y)")} instead? (Yes/No)\n')
                    if alternative_date_answer.lower() == "yes":
                        duration = self.reservations.possible_book_period(nearest_date)
                        if self.make_reservation(name, nearest_date, duration) == 2:
                            continue
                        return 0
                    elif alternative_date_answer.lower() == "no":
                        continue
                    else:
                        print('You have entered incorrect data.')
                        break
            break

    def check_user_reservations_in_week(self, name, entered_datetime):
        if self.reservations.user_reservations_in_week(name, entered_datetime) == 1:
            print('Error, you already have more than two bookings in the given week.')
            return 1
        return 0

    def make_reservation(self, name, entered_datetime, duration):
        if duration == 90:
            duration_answer = input(
                'How long would you like to book court? (1/2/3/4)\n 1) 30 minutes\n 2) 60 minutes\n 3) '
                '90 minutes\n 4) Back\n')
            if duration_answer == "1":
                end_time = entered_datetime + timedelta(seconds=1800)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "2":
                end_time = entered_datetime + timedelta(seconds=3600)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "3":
                end_time = entered_datetime + timedelta(seconds=5400)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "4":
                return 2
            else:
                print('You have entered incorrect data.')
                return 1
        elif duration == 60:
            duration_answer = input(
                'How long would you like to book court? (1/2/3)\n 1) 30 minutes\n 2) 60 minutes\n 3) '
                'Back\n')
            if duration_answer == "1":
                end_time = entered_datetime + timedelta(seconds=1800)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "2":
                end_time = entered_datetime + timedelta(seconds=3600)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "3":
                return 1
            else:
                print('You have entered incorrect data.')
                return 1
        elif duration == 30:
            duration_answer = input('How long would you like to book court? (1/2)\n 1) 30 minutes\n 2) '
                                    'Back\n')
            if duration_answer == "1":
                end_time = entered_datetime + timedelta(seconds=1800)
                self.reservations.new_reservation(name, entered_datetime, end_time)
            elif duration_answer == "2":
                return 1
            else:
                print('You have entered incorrect data.')
                return 1
