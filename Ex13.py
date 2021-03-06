import pytest
import requests


user_agents = [
        (
            {
                'user_agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) '
                              'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                'platform': 'Mobile',
                'browser': 'No',
                'device': 'Android'
            }
        ),
        (
            {
                'user_agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                              'like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
                'platform': 'Mobile',
                'browser': 'Chrome',
                'device': 'iOS'
            }
        ),

        (
            {
                'user_agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'platform': 'Googlebot',
                'browser': 'Unknown',
                'device': 'Unknown'
            }
        ),
        (
            {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
                'platform': 'Web',
                'browser': 'Chrome',
                'device': 'No'
            }
        ),
        (
            {
                'user_agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                              'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'platform': 'Mobile',
                'browser': 'No',
                'device': 'iPhone'
            }
        )
    ]


class TestUserAgent:
    @pytest.mark.parametrize('user_agent', user_agents)
    def test_user_agent(self, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        user_agents_data = user_agent['user_agent']
        expected_platform = user_agent['platform']
        expected_browser = user_agent['browser']
        expected_device = user_agent['device']

        response = requests.get(url, headers={"User-Agent": user_agents_data})
        actual_response = response.json()
        print(actual_response)
        actual_platform = actual_response["platform"]
        actual_browser = actual_response["browser"]
        actual_device = actual_response["device"]

        assert response.status_code == 200, 'Wrong response code'
        assert actual_platform == expected_platform, f"Platform is invalid, expected: {expected_platform}, actual: " \
                                                     f"{actual_platform}"
        assert actual_browser == expected_browser, f"Browser is invalid, expected: {expected_browser}, actual: " \
                                                   f"{actual_browser}"
        assert actual_device == expected_device, f"Device is invalid, expected: {expected_device}, actual: " \
                                                 f"{actual_device}"
