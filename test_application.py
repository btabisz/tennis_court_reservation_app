import io
from application import Application
from datetime import datetime, timedelta
from db_test_data import TestDb
from cancel_reservation_app import CancelReservationApp
from reservation_app import ReservationApp
from reservations import Reservations
import sqlite3
import unittest
from unittest import mock, TestCase
from validations import Validations
from print_app import PrintApp


class FunctionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.res = Reservations()
        cls.val = Validations()
        cls.dbtest = TestDb()
        cls.print = PrintApp()

    def test_name_validation(self):
        self.assertEqual(0, self.val.name_validation("Jan Kowalski"))
        self.assertEqual(1, self.val.name_validation("jan Kowalski"))
        self.assertEqual(1, self.val.name_validation("jan kowalski"))
        self.assertEqual(1, self.val.name_validation("Jan kowalski"))
        self.assertEqual(1, self.val.name_validation("Kowalski"))
        self.assertEqual(1, self.val.name_validation("jan Kowalski"))
        self.assertEqual(0, self.val.name_validation("Alicja Kowalska-Madejska"))
        self.assertEqual(1, self.val.name_validation("Alicja Kowalska Madejska"))
        self.assertEqual(1, self.val.name_validation("alicja kowalska-kadejska"))

    def test_date_validation(self):
        self.assertEqual(1, self.val.date_validation("27:06:2023"))
        self.assertEqual(datetime(2023, 6, 27, 0, 0), self.val.date_validation("27.06.2023"))
        self.assertEqual(1, self.val.date_validation("2023.06.27"))
        self.assertEqual(1, self.val.date_validation("31.06.2023"))
        self.assertEqual(1, self.val.date_validation("29.02.2023"))
        self.assertEqual(1, self.val.date_validation("32.06.2023"))
        self.assertEqual(1, self.val.date_validation("00.06.2023"))
        self.assertEqual(1, self.val.date_validation("01.00.2023"))
        self.assertEqual(datetime(2023, 7, 31, 0, 0), self.val.date_validation("31.07.2023"))

    def test_datetime_validation(self):
        self.assertEqual(1, self.val.datetime_validation("27:06:2023"))
        self.assertEqual(datetime(2023, 6, 27, 14, 0), self.val.datetime_validation("27.06.2023 14:00"))
        self.assertEqual(1, self.val.datetime_validation("2023.06.27 14:00"))
        self.assertEqual(1, self.val.datetime_validation("31.06.2023 14:00"))
        self.assertEqual(1, self.val.datetime_validation("29.02.2023 14:00"))
        self.assertEqual(1, self.val.datetime_validation("32.06.2023 14:00"))
        self.assertEqual(1, self.val.datetime_validation("00.06.2023 14:00"))
        self.assertEqual(datetime(2023, 7, 31, 14, 0), self.val.datetime_validation("31.07.2023 14:00"))
        self.assertEqual(1, self.val.datetime_validation("30.06.2023 25:30"))
        self.assertEqual(1, self.val.datetime_validation("20.02.2023 12:67"))
        self.assertEqual(1, self.val.datetime_validation("20.06.2023 1:00"))
        self.assertEqual(1, self.val.datetime_validation("01.06.2023 12:5"))
        self.assertEqual(2, self.val.datetime_validation("01.06.2023 12:53"))
        self.assertEqual(datetime(2023, 7, 31, 14, 30), self.val.datetime_validation("31.07.2023 14:30"))

    def test_actual_time_validation(self):
        self.assertEqual(0, self.val.actual_time_validation(datetime.now() + timedelta(seconds=3700)))
        self.assertEqual(1, self.val.actual_time_validation(datetime.now() + timedelta(seconds=1800)))
        self.assertEqual(1, self.val.actual_time_validation(datetime.now() - timedelta(days=1)))
        self.assertEqual(0, self.val.actual_time_validation(datetime.now() + timedelta(days=1)))

    def test_user_reservations_in_week(self):
        self.dbtest.insert_test_data()
        self.assertEqual(1, self.res.user_reservations_in_week('Bartosz Polski', (datetime(3023, 4, 13, 14, 0))))
        self.assertEqual(0, self.res.user_reservations_in_week('Kacper Polski', (datetime(3023, 4, 13, 14, 0))))
        self.dbtest.delete_test_data()

    def test_check_court_availability(self):
        self.dbtest.insert_test_data()
        self.assertEqual(1, self.res.check_court_availability(datetime(3023, 4, 13, 14, 0)))
        self.assertEqual(0, self.res.check_court_availability(datetime(3023, 4, 14, 14, 0)))
        self.dbtest.delete_test_data()

    def test_db_date_to_date(self):
        self.assertEqual(datetime(2023, 1, 27), self.val.db_date_to_date('2023-01-27'))
        self.assertEqual(1, self.val.db_date_to_date('ddddddddddd'))
        self.assertEqual(1, self.val.db_date_to_date('06.01.2023'))

    def test_db_datetime_to_datetime(self):
        self.assertEqual(datetime(2023, 1, 27, 14, 0), self.val.db_datetime_to_datetime('2023-01-27 14:00'))
        self.assertEqual(1, self.val.db_datetime_to_datetime('date, time'))
        self.assertEqual(1, self.val.db_datetime_to_datetime('06.01.2023'))

    def test_check_leap_year(self):
        self.assertEqual(False, self.val.check_leap_year('2023'))
        self.assertEqual(True, self.val.check_leap_year('2024'))

    def test_start_hour_validation(self):
        self.assertEqual(0, self.val.start_hour_validation(datetime(2023, 1, 27, 14, 0)))
        self.assertEqual(0, self.val.start_hour_validation(datetime(2023, 1, 27, 14, 30)))
        self.assertEqual(1, self.val.start_hour_validation(datetime(2023, 1, 27, 14, 10)))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_date(self, mock_stdout):
        self.print.print_date(datetime.now())
        self.assertEqual('\nToday:\n', mock_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_printer(self, mock_stdout):
        self.dbtest.insert_test_data()
        self.print.printer(datetime(3023, 4, 14), datetime(3023, 4, 14))
        expected = '\nMonday, 14. April 3023:\n* Bartosz Polski 19:00 - 20:00\n-------------------------\n'
        self.assertEqual(expected, mock_stdout.getvalue())
        self.dbtest.delete_test_data()

    def test_new_reservation(self):
        self.assertEqual(0, self.res.new_reservation("Maciej Polit", datetime(3023, 4, 11, 12, 0),
                                                     datetime(3023, 4, 11, 12, 30)))
        self.delete_from_db("Maciej Polit", datetime(3023, 4, 11, 12, 0))

    def test_get_nearest_date(self):
        self.dbtest.insert_test_data()
        self.assertEqual(datetime(3023, 4, 13, 17, 0), self.res.get_nearest_date(datetime(3023, 4, 13, 16, 0)))
        self.dbtest.delete_test_data()

    @staticmethod
    def delete_from_db(name, date):
        conn = sqlite3.connect('./db.sqlite')
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", (name, date))
        conn.commit()
        conn.close()
        print('Deleted form db')


class AppsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Application()
        cls.res_app = ReservationApp()
        cls.can_res_app = CancelReservationApp()

    @mock.patch('builtins.input', create=True)
    def test_reservationApp_success(self, mocked_input):
        mocked_input.side_effect = ['Bartosz Tabisz', '25.07.2999 14:30', '2']
        result = self.res_app.start_reservation_app()
        self.delete_from_db('Bartosz Tabisz', '2999-07-25 14:30:00')
        self.assertEqual(0, result)

    @mock.patch('builtins.input', create=True)
    def test_CancelReservationApp_success(self, mocked_input):
        mocked_input.side_effect = ['Kamil Kasperczak', '25.07.2999 14:30', '2']
        self.res_app.start_reservation_app()
        mocked_input.side_effect = ['Kamil Kasperczak', '25.07.2999 14:30']
        result = self.can_res_app.start_cancel_reservation_app()
        self.assertEqual(0, result)

    @staticmethod
    def delete_from_db(name, date):
        conn = sqlite3.connect('./db.sqlite')
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", (name, date))
        conn.commit()
        conn.close()
        print('Deleted form db')


if __name__ == '__main__':
    unittest.main()
