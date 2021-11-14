import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ["POST", "GET", "PUT", "DELETE"]

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response_1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Результат запроса без параметра: {response_1.text}")

# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response_2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"Результат запроса параметром не из списка: {response_2.text}")

# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response_3 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print(f"Результат запроса с правильным значением method: {response_3.text}")

# 4. Циклы.
for request_method in methods:
    for params_method in methods:
        if request_method == "GET":
            response = requests.request(method=request_method, url=url, params={"method": params_method})
        else:
            response = requests.request(method=request_method, url=url, data={"method": params_method})

        if request_method == params_method and response.text != response_3.text:
            print(f"При методе {request_method} и параметре {params_method}")
            print(f"Ожидается такое: {response_3.text}")
            print(f"А получается вот так: {response_1.text}")
        elif request_method != params_method and response.text == response_3.text:
            print(f"При методе {request_method} и параметре {params_method}")
            print(f"Ожидается такое: {response_1.text}")
            print(f"А получается вот так: {response_3.text}")
