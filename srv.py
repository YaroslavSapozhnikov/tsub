import datetime
import requests

# Базовый URL
BASE_URL = "http://yar.diskstation.me:8001"

# ID объекта, который нужно обновить
facility_id = 0  # Замените на нужный ID


class Srv(object):
    def __init__(self, name: str, port: int = 8000):
        self.url = f"http://{name}:{port}"

    def request(self, facility: dict):
        url = f"{self.url}/facilities/{facility["id"]}"

        if facility["update_time"] is None:
            facility["update_time"] = datetime.now().replace(microsecond=0)
        # Отправляем PUT-запрос с JSON-данными
        response = requests.put(url, json=facility)

        # Проверяем ответ
 #       if response.status_code == 200:
 #           print("PUT-запрос выполнен успешно")
 #           print("Ответ сервера:", response.json())
 #       else:
 #           print(f"Ошибка: {response.status_code}")
 #           print("Текст ответа:", response.text)


if __name__ == '__main__':
    pass
