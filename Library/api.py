import json
import re
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
                allure.attach(str(expected_json), name="Expected JSON")
                if Var.env("snap") == "1":
                    yaml_load[key_name] = Store.current_response.json()
                Api.dump_in_dynamic_variable_file(file_path, yaml_load)
            except Exception as e:
                allure.attach(str(e), name="Error while fetching the key from expected yaml file")
                if Var.env("snap") == "1":
                    yaml_load[key_name] = Store.current_response.json()
                Api.dump_in_dynamic_variable_file(file_path, yaml_load)
            assert (Api.json_compare(expected_json, Store.current_response.json())), \
                "Response doesn't match with stored json \nExpected: " + str(expected_json) + \
                "\nActual response: " + str(Store.current_response.json())

    @staticmethod
    def ignore_keys(keys):
        Store.ignore_keys = keys.split(",")

    @staticmethod
    def json_compare(json1, json2):
        ignore_keys = Store.ignore_keys
        allure.attach(str(ignore_keys), name="Keys Ignored while comparing")
        d1_filtered = dict((k, v) for k, v in json1.items() if k not in ignore_keys)
        d2_filtered = dict((k, v) for k, v in json2.items() if k not in ignore_keys)
        for k, v in d1_filtered.items():
            if v == "$notnull":
                assert (d2_filtered[k] != "Null"), "Key value " + k + " is null in response"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$null":
                assert (d2_filtered[k] == "Null"), "Key value " + k + " is not null in response"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$array":
                assert (type(d2_filtered[k]) in (tuple, list) is True), "Key " + k + " is not in array format"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$json":
                try:
                    json.loads(d2_filtered[k])
                    result = True
                except ValueError as e:
                    print(e)
                    result = False
                assert (result is True), "Key " + k + " is not in json format"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$boolean":
                result = type(d2_filtered[k]) is bool
                assert (result is True), "Key " + k + " is not in boolean format"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$number":
                result = isinstance(d2_filtered[k], (int, float, complex)) and not isinstance(d2_filtered[k], bool)
                assert (result is True), "Key " + k + " is not in number format"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$string":
                result = isinstance(d2_filtered[k], str)
                assert (result is True), "Key " + k + " is not in string format"
                d1_filtered[k] = d2_filtered[k]
            elif v == "$uuid":
                uuid_pattern = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
                result = uuid_pattern.match(d2_filtered[k])
                assert (result is True), "Key " + k + " is not in uuid format"
                d1_filtered[k] = d2_filtered[k]
        return d1_filtered == d2_filtered

    @staticmethod
    def get_params_from_response(path):
        path_array = path.split(",")
        result = Store.current_response.json()
        for key in path_array:
            result = result[key]
        return result
