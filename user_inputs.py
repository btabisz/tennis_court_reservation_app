from validations import Validations


class UserInputsApp:
    def __init__(self):
        self.validations = Validations()

    def get_start_datetime(self, title):
        while True:
            if title == "book":
                date = input("When would you like to book? {DD.MM.YYYY HH:MM}\n")
            else:
                date = input("When would you like to cancel? {DD.MM.YYYY HH:MM}\n")
            entered_datetime = self.validations.datetime_validation(date)
            if not isinstance(entered_datetime, int):
                return entered_datetime
            if entered_datetime == 1:
                if self.incorrect_format() == 1:
                    return 1
                continue
            if entered_datetime == 2:
                incorrect_date_answer = input('Court rental can only start at full hour or half hour. Do you want '
                                              'to resubmit? (Yes/No)\n')
                if incorrect_date_answer.lower() == "yes":
                    continue
                elif incorrect_date_answer.lower() == "no":
                    return 1
                else:
                    print('You have entered incorrect data.')
                    return 1

    def get_name(self):
        while True:
            name = input("What's your Name? (full name)\n")
            if self.validations.name_validation(name) == 0:
                return name
            if self.validations.name_validation(name) == 1:
                if self.incorrect_format() == 1:
                    return 1
                continue

    def get_date(self, title):
        while True:
            if title == "start":
                date = input("Enter schedule start time? {DD.MM.YYYY}\n")
            else:
                date = input("Enter schedule end time? {DD.MM.YYYY}\n")
            schedule_start_date = self.validations.date_validation(date)
            if not isinstance(schedule_start_date, int):
                return schedule_start_date
            if schedule_start_date == 1:
                if self.incorrect_format() == 1:
                    return 1
                continue

    def get_file_name(self):
        while True:
            file_name = input("Enter file name?\n")
            if self.validations.file_name_validation(file_name) == 0:
                return file_name
            if self.validations.name_validation(file_name) == 1:
                print(self.incorrect_format())
                if self.incorrect_format() == 1:
                    return 1
                continue

    @staticmethod
    def incorrect_format():
        incorrect_answer = input('Incorrect format. Do you want to resubmit? (Yes/No)\n')
        if incorrect_answer.lower() == "yes":
            return 0
        elif incorrect_answer.lower() == "no":
            return 1
        else:
            print('You have entered incorrect data.')
            return 1
