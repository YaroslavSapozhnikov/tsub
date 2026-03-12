import requests

# Базовый URL
BASE_URL = "http://yar.diskstation.me:8001"

# ID объекта, который нужно обновить
facility_id = 0  # Замените на нужный ID

# Тело запроса
data = {
    "id": 0,
    "name": "string",
    "addr": "string",
    "sensors": [
        {
            "name": "Датчик 1",
            "addr": 10,
            "input": 0,
            "readout": "99.5"
        },
        {
            "name": "Датчик 2",
            "addr": 10,
            "input": 1,
            "readout": "50.0"
        }
    ],
    "update_time": "2026-03-11T21:12:12.161Z"
}

if __name__ == '__main__':
    # Формируем полный URL с указанием ID
    url = f"{BASE_URL}/facilities/{facility_id}"

    # Отправляем PUT-запрос с JSON-данными
    response = requests.put(url, json=data)

    # Проверяем ответ
    if response.status_code == 200:
        print("PUT-запрос выполнен успешно")
        print("Ответ сервера:", response.json())
    else:
        print(f"Ошибка: {response.status_code}")
        print("Текст ответа:", response.text)
