import random
import string
import requests
from api_test.data import BASE_URL, COURIERS_URL

def create_courier_payload(register_courier):
    """Создает payload для курьера на основе данных зарегистрированного курьера."""
    return {
        "login": register_courier["login"],
        "password": register_courier["password"],
        "firstName": register_courier["first_name"]
    }

def send_create_courier_request(payload):
    """Отправляет POST-запрос для создания курьера и возвращает ответ."""
    response = requests.post(f'{BASE_URL}{COURIERS_URL}', json=payload)
    return response

def check_response_status(response, expected_status_code):
    """Проверяет статус ответа."""
    assert response.status_code == expected_status_code, (
        f"Ожидался статус код {expected_status_code}, но получен {response.status_code}."
    )

def check_response_body(response, expected_response):
    """Проверяет тело ответа."""
    assert response.json() == expected_response, (
        f"Ожидался ответ {expected_response}, но получен {response.json()}."
    )

def create_courier_with_login(payload):
    """Создает курьера и возвращает его логин для последующих запросов."""
    response = send_create_courier_request(payload)
    check_response_status(response, 201)  # Убедитесь, что создание прошло успешно
    check_response_body(response, {"ok": True})
    return payload["login"]  # Возвращаем логин для использования в дублирующем запросе

def generate_random_string(length=10):
    """Генерирует случайную строку фиксированной длины."""
    letters = string.ascii_letters + string.digits  # Можно использовать буквы и цифры
    return ''.join(random.choice(letters) for _ in range(length))

