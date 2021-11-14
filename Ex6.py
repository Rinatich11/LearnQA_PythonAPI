import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
final_response = response

print(len(response.history))
print(final_response.url)