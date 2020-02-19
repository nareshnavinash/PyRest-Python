import os
import yaml
import allure
from Library.store import Store


class Var:
    file_name = None
    static_variable = None
    dynamic_variable = None
    file_path = None
    static_data_path = Store.static_data_path
    dynamic_data_path = Store.dynamic_data_path
    global_data_path = Store.global_data_path

    def __init__(self, file_name, type):
        self.file_name = file_name
        if type == "static":
            try:
                self.file_path = self.static_data_path + '/' + file_name
                with open(self.file_path) as file:
                    self.static_variable = yaml.load(file, Loader=yaml.FullLoader)
                allure.attach.file(self.file_path, name=self.file_name, attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                print(e)
        if type == "dynamic":
            try:
                self.file_path = self.dynamic_data_path + '/' + file_name
                if not os.path.isfile(self.file_path):
                    if str(self.env("snap")) == "1":
                        f = open(self.file_path, "w")
                        f.close()
                with open(self.file_path) as file:
                    self.dynamic_variable = yaml.load(file, Loader=yaml.FullLoader)
                allure.attach.file(self.file_path, name=self.file_name, attachment_type=allure.attachment_type.TEXT)
            except IOError as e:
                print("File is not accessible\n" + str(e))
            except Exception as e:
                print(e)

    @staticmethod
    def env(string):
        try:
            return os.environ[string]
        except Exception as e:
            print(e)
            return "None"

    @staticmethod
    def glob(string):
        try:
            with open(Var.global_data_path) as file:
                global_data = yaml.load(file, Loader=yaml.FullLoader)
                return global_data[string]
        except Exception as e:
            print(e)
            return "None"

    def static_value_for(self, string) -> str:
        try:
            return self.static_variable[string]
        except Exception as e:
            print(e)
            return ""

    def write(self, params):
        if self.env("snap") == "1":
            with open(self.file_path, 'w') as file:
                documents = yaml.dump(params, file)
                print(documents)

    def dynamic_value_for(self, string) -> str:
        try:
            return self.dynamic_variable[string]
        except Exception as e:
            print(e)
            return ""

    def compare(self, displayed_variable):
        if self.env("snap") == "1":
            self.write(displayed_variable)
        for key, value in displayed_variable.items():
            try:
                file_value = self.dynamic_variable[key]
            except Exception as e:
                print(e)
                file_value = "key_not_available"
            if file_value == "key_not_available":
                with allure.step("Verifying the key: " + str(key)):
                    assert (file_value == value), "Key is not available in the dynamic data file\n Key:- " + key \
                                                  + "\nTo store the displayed value try running the suite with\n" \
                                                  + "snap=1 pytest"
            else:
                with allure.step("Verifying the key: " + str(key)):
                    assert (str(file_value) == str(value)), "Value for the Key:- " + str(key) + ", Mismatches\n" \
                                                  + "File Value:- " + str(file_value) \
                                                  + "\nDisplayed Value:- " + str(value) \
                                                  + "\nFile used for validation is:" + self.file_name \
                                                  + "\nTo change the Dynamic file value run the suite with" \
                                                  + "\nsnap=1 pytest"
