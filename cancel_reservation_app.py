from reservations import Reservations
from user_inputs import UserInputsApp
from validations import Validations


class CancelReservationApp:
    def __init__(self):
        self.reservations = Reservations()
        self.validations = Validations()
        self.inputs = UserInputsApp()

    def start_cancel_reservation_app(self):
        print("Cancel a reservation")
        while True:
            name = self.inputs.get_name()
            if name == 1:
                break
            entered_datetime = self.inputs.get_start_datetime("cancel")
            if entered_datetime == 1:
                break
            if self.validations.actual_time_validation(entered_datetime) == 1:
                print('Error, booking cannot be canceled if it is less than an hour before the start time!')
                break
            if self.reservations.cancel_reservation(name, entered_datetime) == 1:
                incorrect_cancel_answer = input('Reservation not found. Do you want to resubmit? (Yes/No)\n')
                if incorrect_cancel_answer.lower() == "yes":
                    continue
                elif incorrect_cancel_answer.lower() == "no":
                    break
                else:
                    print('You have entered incorrect data.')
                    break
            else:
                return 0
