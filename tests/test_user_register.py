from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

excluded_params = [
    ("email"),
    ("password"),
    ("firstName"),
    ("lastName"),
    ("username")
]


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/",data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vinkotovexample.com'
        my_data = self.prepare_registration_data(incorrect_email)
        response = MyRequests.post("/user/", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "Invalid email format")

    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_create_user_without_one_params(self, missed_field):
        my_data = self.prepare_registration_data()
        del my_data[f"{missed_field}"]
        response = MyRequests.post("/user", data=my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response,
                                                    f"The following params are missed: {missed_field}")

    def test_create_user_with_too_short_name(self):
        my_data = self.prepare_registration_data()
        my_data["username"] = "a"
        response = MyRequests.post("/user", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "The value of 'username' field is too short")

    def test_create_user_with_too_long_name(self):
        my_data = self.prepare_registration_data()
        my_data["username"] = 251 * "a"
        response = MyRequests.post("/user", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "The value of 'username' field is too long")