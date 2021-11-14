import requests
import time

# 1) создавал задачу
response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
parsed_response_text = response_1.json()
needed_token = parsed_response_text["token"]
print(parsed_response_text["seconds"])
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": needed_token})
print(response_2.text)
# 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
time.sleep(parsed_response_text["seconds"] + 1)
# 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля
# result
response_3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": needed_token})
parsed_response_text_2 = response_3.json
print(response_3.text)
