import requests

class TestFirstCookie:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response1 = requests.get(url)

        cookie = response1.cookies
        print(cookie)

        response2 = response1
        assert response2.cookies == cookie, "Cookie is invalid"
