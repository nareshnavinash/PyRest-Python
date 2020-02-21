import allure
import requests
from Library.variable import Var
from Library.store import Store


class Api:
    URL = None
    endpoint = None
    params = None
    response = None

    def __init__(self, url):
        Api.URL = url

    @classmethod
    def get(cls, **kwargs):
        response = requests.get(Api.URL + Api.endpoint, Api.params, **kwargs)
        allure.step("Response for Get with " + Api.endpoint)
        allure.step("Get request Prams " + str(Api.params))
        allure.step("Other get Args " + str(**kwargs))
        allure.attach(response.status_code, name="Response Status Code")
        allure.attach(response.headers, name="Response Headers")
        allure.attach(response.text, name="Response Text")
        allure.attach(response.json(), name="Response JSON")
        Api.response = response

    @classmethod
    def set_end_point(cls, endpoint):
        Api.endpoint = endpoint

    @classmethod
    def set_params(cls, params):
        Api.params = params
