from reservations import Reservations
from save import Save
from user_inputs import UserInputsApp
from validations import Validations


class SaveApp:
    def __init__(self):
        self.reservations = Reservations()
        self.validations = Validations()
        self.save = Save()
        self.inputs = UserInputsApp()

    def start_save_app(self):
        while True:
            save_start_date = self.inputs.get_date("start")
            if save_start_date == 1:
                break
            save_end_date = self.inputs.get_date("end")
            if save_end_date == 1:
                break
            if save_start_date > save_end_date:
                print('You have entered wrong dates.')
                continue
            file_name = self.inputs.get_file_name()
            if file_name == 1:
                break
            file_format = input('What format do you want to save the data in? (csv/json)\n')
            if file_format == "csv":
                self.save.save_to_csv(save_start_date, save_end_date, file_name)
                print(f'A {file_name}.csv file has been generated.')
                break
            if file_format == "json":
                self.save.save_to_json(save_start_date, save_end_date, file_name)
                print(f'A {file_name}.json file has been generated.')
                break
            else:
                print('You have entered incorrect data.')
                break
