import requests

class TestFirstHeaders:
    def test_homework_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"

        response1 = requests.get(url)

        headers = response1.headers
        print(headers)
        assert headers is not None, "Headers are invalid"
