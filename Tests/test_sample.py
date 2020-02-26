import allure
import pytest
from Library.api import Api
from Library.images import Img


@allure.feature("Sample get request")
@allure.severity('Critical')
@pytest.mark.regression  # Custom pytest marker to run the test cases with ease on demand
@pytest.mark.snap  # Custom pytest marker to run the test cases with ease on demand
def test_sample_get_request_001():
    Api.get("/name")
    Api.verify_response_code(200)
    Api.ignore_keys("age")
    Api.verify_response_json("sample.yml", "test_sample_get_request_001")


@allure.feature("Sample get request with custom params")
@allure.severity('Critical')
@pytest.mark.regression  # Custom pytest marker to run the test cases with ease on demand
@pytest.mark.plain  # Custom pytest marker to run the test cases with ease on demand
def test_sample_get_request_002():
    Api.get("/name")
    Api.verify_response_code(200)
    Api.ignore_keys("age")
    Api.verify_response_json("sample.yml", "test_sample_get_request_002")


@allure.feature("Sample get request with image URL")
@allure.severity('Critical')
@pytest.mark.regression  # Custom pytest marker to run the test cases with ease on demand
@pytest.mark.snap  # Custom pytest marker to run the test cases with ease on demand
def test_sample_get_request_003():
    Api.get("/image")
    Api.verify_response_code(200)
    Api.ignore_keys("age")
    Api.verify_response_json("sample.yml", "test_sample_get_request_003")
    image_url = Api.get_params_from_response("image")
    Img.download_image(image_url, "Naresh")
    Img.is_equal("Naresh", "Naresh")
