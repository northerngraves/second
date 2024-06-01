import requests

# URL API
url = "https://api.puzzlebot.top/"

# Параметры запроса
params = {
    'token': '0O61PQUHwCHgK2INgiBjuH7AphSk6PLB',
    'method': 'postSend'
}

data = {
    "chats_ids": "private",
    "text": "Привет от Артура)))\nСюда будут приходить заказы с сайта.\nНадеюсь все работает c:",
    "type": "message"
}

# Отправка POST-запроса
response = requests.post(url, params=params, json=data)

# Проверка ответа
if response.status_code == 200:
    print("Запрос успешно выполнен!")
    print("Ответ сервера:", response.json())
else:
    print("Ошибка в запросе:", response.status_code)