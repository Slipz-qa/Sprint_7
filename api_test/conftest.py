import pytest
import requests
import random
import string
from api_test.data import BASE_URL, COURIERS_URL, COURIER_DATA, ORDERS_URL
from api_test.methods.login_courier_methods import LoginCourier


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


login_courier = LoginCourier()

@pytest.fixture()
def register_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}{COURIERS_URL}', json=payload)

    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "first_name": first_name,
            "id": response.json().get("id")
        }
    else:
        pytest.fail(f"Не удалось создать курьера. Код ответа: {response.status_code}, Сообщение: {response.json()}")

@pytest.fixture()
def cleanup_courier(request):
    courier_data = request.getfixturevalue('register_courier')

    yield
    if courier_data and "id" in courier_data:
        print(f"Попытка удалить курьера с ID: {courier_data['id']}")

        check_response = requests.get(f'{BASE_URL}{COURIERS_URL}/{courier_data["id"]}')
        if check_response.status_code == 200:
            delete_response = requests.delete(f'{BASE_URL}{COURIERS_URL}/{courier_data["id"]}')
            print(f"Статус ответа при удалении: {delete_response.status_code}, Сообщение: {delete_response.text}")
            assert delete_response.status_code == 200, "Не удалось удалить курьера."
        else:
            print(f"Курьер не найден для удаления, статус: {check_response.status_code}")

@pytest.fixture(scope="module")
def register_courier_with_data():

    response = login_courier.send_create_request(COURIER_DATA)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.json()}"
    return COURIER_DATA


@pytest.fixture()
def create_order(color):
    order_data = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": [color]  # Указываем цвет из параметра
    }

    response = requests.post(f"{BASE_URL}{ORDERS_URL}", json=order_data)

    if response.status_code == 201:
        return response.json()
    else:
        pytest.fail(f"Не удалось создать заказ. Код ответа: {response.status_code}, Сообщение: {response.json()}")


@pytest.fixture()
def order_data():
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }





