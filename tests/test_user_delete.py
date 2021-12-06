from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


class TestUserDelete(BaseCase):
    def test_delete_protected_user(self):
        user_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=user_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(f"/user/2",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_expected_response_content(response2,
                                                    "Do not delete test users with ID 1, 2, 3, 4 or 5.")

    def test_delete_user_successfully(self):
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

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_expected_response_content(response4, "User not found")

    def test_delete_user_auth_as_another_user(self):
        # REGISTER user1
        response1, registration_data1 = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = registration_data1['email']
        password1 = registration_data1['password']
        time.sleep(5)

        # REGISTER user2
        response2, registration_data2 = self.generate_new_user()

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = registration_data2['email']
        password2 = registration_data2['password']
        user2_id = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # DELETE user2 by user1
        MyRequests.delete(f"/user/{user2_id}",
                          headers={"x-csrf-token": token1},
                          cookies={"auth_sid": auth_sid1}
                          )
        # LOGIN as user2
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data2)
        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        # GET user2 data
        response6 = MyRequests.get(f"/user/{user2_id}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2}
                                   )
        Assertions.assert_json_has_key(response6, "id")
