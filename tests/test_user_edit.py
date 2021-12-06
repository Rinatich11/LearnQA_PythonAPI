from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    # Changing user data (unauthorized)
    def test_edit_not_auth_user(self):
        new_name = "Changed_Name"
        response1 = MyRequests.put("/user/2",
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response1, 400)
        Assertions.assert_expected_response_content(response1, "Auth token not supplied")

    # Changing user data with authorized another user
    def test_edit_user_auth_as_another_user(self):
        # REGISTER user1
        response1, registration_data1 = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = registration_data1['email']
        password1 = registration_data1['password']

        # REGISTER user2
        response2, registration_data2 = self.generate_new_user()

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = registration_data2['email']
        password2 = registration_data2['password']
        first_name2 = registration_data2['firstName']
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data1 = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data1)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "changed name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token1},
                                   cookies={"auth_sid": auth_sid1},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_code_status(response4, 200)

        # LOGIN as user2
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        # GET user2 data
        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2}
                                   )

        Assertions.assert_json_value_by_name(response6,
                                             "firstName",
                                             first_name2,
                                             f"Name of the user was edited by another user!"
                                             )

    incorrect_data = [
        ({'email': "incorrect_email.com"}, (400, "Invalid email format")),
        ({'firstName': "c"}, (400, "Too short value for field firstName"))
    ]

    # Changing user data with incorrect email and firstName
    @pytest.mark.parametrize("input_data, expected_result", incorrect_data)
    def test_edit_user_with_incorrect_data(self, input_data, expected_result):
        # REGISTER
        response1, registration_data = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registration_data['email']
        password = registration_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data=input_data
                                   )
        expected_status_code, expected_text = expected_result
        Assertions.assert_code_status(response3, expected_status_code)
        assert expected_text in response3.text
