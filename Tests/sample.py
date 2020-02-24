import allure
import pytest
from Library.api import Api


@allure.feature("Sample get request")
@allure.severity('Critical')
@pytest.mark.regression  # Custom pytest marker to run the test cases with ease on demand
@pytest.mark.snap  # Custom pytest marker to run the test cases with ease on demand
def test_sample_get_request_001():
    Api.get("/name")
    Api.verify_response_code(200)
    Api.verify_response_json("sample.yml", "test_sample_get_request_001")
