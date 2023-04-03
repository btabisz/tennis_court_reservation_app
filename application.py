from cancel_reservation_app import CancelReservationApp
from print_app import PrintApp
from reservation_app import ReservationApp
from save_app import SaveApp


class Application:
    def __init__(self):
        self.reservation_app = ReservationApp()
        self.cancel_reservation = CancelReservationApp()
        self.print = PrintApp()
        self.save = SaveApp()
        print('Welcome to the tennis court booking app!')

    def start_app(self):
        options = {'1': self.reservation_app.start_reservation_app,
                   '2': self.cancel_reservation.start_cancel_reservation_app,
                   '3': self.print.start_print_app,
                   '4': self.save.start_save_app}
        while True:
            choice = input(
                'What do you want to do:\n1) Make a reservation\n2) Cancel a reservation\n3) Print schedule\n4) Save '
                'schedule to a file\n5) Exit\n')
            try:
                options[choice]()
            except KeyError:
                exit(0)


def main():
    app = Application()
    app.start_app()


if __name__ == '__main__':
    main()
