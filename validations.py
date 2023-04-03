from datetime import datetime
import re


class Validations:
    def __init__(self):
        pass

    @staticmethod
    def file_name_validation(file_name):
        regex = r'^[A-Za-z0-9]+[A-Za-z0-9-._/\s:]*[A-Za-z0-9]*$'
        if re.search(regex, file_name):
            return 0
        else:
            return 1

    @staticmethod
    def name_validation(name):
        regex = r'^[A-ZĄĘÓŻŹĆŃŁŚ][a-ząęóżźćńłś]+[\s][A-ZĄĘÓŻŹĆŃŁŚ][a-ząęóżźćńłś]+[-]?[A-ZĄĘÓŻŹĆŃŁŚ]?[a-ząęóżźćńłś]*$'
        if re.search(regex, name):
            return 0
        else:
            return 1

    def date_validation(self, time):
        try:
            if self.check_leap_year(time[6:10]) and int(time[3:5]) == 2:
                regex = r'^([1-2][0-9]|[0-2][1-9])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9]$'
            elif int(time[3:5]) == 2:
                regex = r'^([1-2][0-8]|[0-2][1-8])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9]$'
            elif int(time[3:5]) in [1, 3, 5, 7, 8, 10, 12]:
                regex = r'^([1-2][0-9]|[0-2][1-9]|[3][0-1])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9]$'
            else:
                regex = r'^([1-2][0-9]|[0-2][1-9]|[3][0])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9]$'
            if re.search(regex, time):
                return self.get_entered_date(time)
            else:
                return 1
        except ValueError:
            return 1

    def datetime_validation(self, start_time):
        try:
            if self.check_leap_year(start_time[6:10]) and int(start_time[3:5]) == 2:
                regex = r'^([1-2][0-9]|[0-2][1-9])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9][\s]([0-1][0-9]|[2][' \
                        r'0-4])[:][0-5][0-9]$'
            elif int(start_time[3:5]) == 2:
                regex = r'^([1-2][0-8]|[0-2][1-8])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9][\s]([0-1][0-9]|[2][' \
                        r'0-4])[:][0-5][0-9]$'
            elif int(start_time[3:5]) in [1, 3, 5, 7, 8, 10, 12]:
                regex = r'^([1-2][0-9]|[0-2][1-9]|[3][0-1])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9][\s]([0-1][' \
                        r'0-9]|[2][0-4])[:][0-5][0-9]$'
            else:
                regex = r'^([1-2][0-9]|[0-2][1-9]|[3][0])[.]([0][1-9]|[1][0-2])[.][0-9][0-9][0-9][0-9][\s]([0-1][' \
                        r'0-9]|[2][0-4])[:][0-5][0-9]$'
            if re.search(regex, start_time):
                if self.start_hour_validation(self.get_entered_datetime(start_time)) == 0:
                    return self.get_entered_datetime(start_time)
                else:
                    return 2
            else:
                return 1
        except ValueError:
            return 1

    @staticmethod
    def check_leap_year(year):
        if (int(year) % 4 == 0) and (int(year) % 100 != 0) or (int(year) % 400 == 0):
            return True
        else:
            return False

    @staticmethod
    def actual_time_validation(entered_datetime):
        datetime_difference = entered_datetime - datetime.now()
        if datetime_difference.total_seconds() >= 3600:
            return 0
        else:
            return 1

    @staticmethod
    def start_hour_validation(entered_datetime):
        if entered_datetime.strftime('%M') == "00" or entered_datetime.strftime('%M') == "30":
            return 0
        else:
            return 1

    @staticmethod
    def get_entered_datetime(date):
        try:
            entered_day = int(date[0:2])
            entered_month = int(date[3:5])
            entered_year = int(date[6:10])
            entered_hour = int(date[11:13])
            entered_minute = int(date[14:16])

            entered_datetime = datetime(entered_year, entered_month, entered_day, entered_hour, entered_minute, 0)
            return entered_datetime
        except ValueError:
            return 1

    @staticmethod
    def get_entered_date(date):
        try:
            entered_day = int(date[0:2])
            entered_month = int(date[3:5])
            entered_year = int(date[6:10])

            entered_date = datetime(entered_year, entered_month, entered_day, 0, 0, 0)
            return entered_date
        except ValueError:
            return 1

    @staticmethod
    def db_date_to_date(date):
        try:
            db_year = int(date[0:4])
            db_month = int(date[5:7])
            db_day = int(date[8:10])

            date = datetime(db_year, db_month, db_day)
            return date
        except ValueError:
            return 1

    @staticmethod
    def db_datetime_to_datetime(date):
        try:
            db_year = int(date[0:4])
            db_month = int(date[5:7])
            db_day = int(date[8:10])
            db_hour = int(date[11:13])
            db_minute = int(date[14:16])

            date = datetime(db_year, db_month, db_day, db_hour, db_minute, 0)
            return date
        except ValueError:
            return 1
