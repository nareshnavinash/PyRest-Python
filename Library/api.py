import allure
import requests
import yaml
import os.path

from Library.variable import Var
from Library.store import Store


class Api:

    @staticmethod
    def get(endpoint, params=None, **kwargs):
        url = Var.current("URL")
        with allure.step("Get request with the url " + url + endpoint):
            response = requests.get(url + endpoint, params, **kwargs)
        with allure.step("Response for Get with " + endpoint + " " + str(params)):
            allure.attach(str(**kwargs), name="Other arguments passed for get request")
            allure.attach(str(response.status_code), name="Response Status Code")
            allure.attach(str(response.headers), name="Response Headers")
            allure.attach(str(response.text), name="Response Text")
            allure.attach(str(response.json()), name="Response JSON")
            Store.current_response = response
            return response

    @staticmethod
    def verify_response_code(status_code):
        with allure.step("Validating the status code for the request"):
            result = Store.current_response.status_code == status_code
            assert (result is True), "Response status code is not matched, \n" \
                                     "expected: " + status_code + "\n" \
                                     "actual: " + Store.current_response.status_code

    @staticmethod
    def create_file_if_not_present(file_path):
        if Var.env("snap") == "1":
            if not os.path.isfile(file_path):
                with open(file_path, 'w') as file:
                    documents = yaml.dump({'created_from': 'snap mode in pyrest framework'}, file)
                    print(documents)

    @staticmethod
    def dump_in_dynamic_variable_file(file_path, params):
        if Var.env("snap") == "1":
            with open(file_path, 'w') as file:
                documents = yaml.dump(params, file)
                print(documents)

    @staticmethod
    def verify_response_json(file_name, key_name):
        expected_json = {}
        file_path = Var.root_path() + "/Data/DynamicData/" + file_name
        Api.create_file_if_not_present(file_path)
        with open(file_path) as file:
            yaml_load = yaml.load(file, Loader=yaml.FullLoader)
        with allure.step("Validating the response json with stored value"):
            allure.attach.file(file_path, name=file_name, attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(Store.current_response.json()), name="Response JSON")
            try:
                expected_json = yaml_load[key_name]
                if Var.env("snap") == "1":
                    yaml_load[key_name] = Store.current_response.json()
                Api.dump_in_dynamic_variable_file(file_path, yaml_load)
            except Exception as e:
                allure.attach(str(e), name="Error while fetching the key from expected yaml file")
                if Var.env("snap") == "1":
                    yaml_load[key_name] = Store.current_response.json()
                Api.dump_in_dynamic_variable_file(file_path, yaml_load)
            assert (expected_json == Store.current_response.json()), "Expected Json doesn't match with stored json" \
                                                                     "file \nExpected: " + str(expected_json) + "\n" \
                                                                     "Actual response: " \
                                                                     "" + str(Store.current_response.json())
