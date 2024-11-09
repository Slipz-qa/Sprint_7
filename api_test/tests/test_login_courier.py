import pytest
from api_test.methods.login_courier_methods import LoginCourier


login_courier = LoginCourier()

@pytest.mark.parametrize("payload, expected_status_code", [
    ({"login": "test_login", "password": "test_password"}, 200),
])
def test_login_courier(register_courier, payload, expected_status_code):
    payload = {
        "login": register_courier["login"],
        "password": register_courier["password"]
    }

    response = login_courier.send_login_request(payload)

    assert response.status_code == expected_status_code, (
        f"Ожидался статус код {expected_status_code}, но получен {response.status_code}."
    )

    response_body = response.json()
    assert "id" in response_body, "Ответ не содержит ключ 'id'."
    assert isinstance(response_body["id"], int), "Значение 'id' должно быть целым числом."


@pytest.mark.parametrize("login, password, expected_status_code", [
    ("wrong_login", "test", 404),
    ("Artem", "wrong_password", 404),
])
def test_login_courier_invalid_credentials(register_courier, login, password, expected_status_code):
    payload = {
        "login": login,
        "password": password
    }

    response = login_courier.send_login_request(payload)

    assert response.status_code == expected_status_code, (
        f"Ожидался статус код {expected_status_code}, но получен {response.status_code}."
    )


@pytest.mark.parametrize("payload, expected_status_code", [
    ({"password": "test"}, 400), #Код ответа выдает 400 или 504 вне зависимости от написанного кода. Я оставил ожидаемое значение 400 из докуентации к API по совету наставника
    ({"login": "Artem"}, 400), #Код ответа выдает 400 или 504 вне зависимости от написанного кода. Я оставил ожидаемое значение 400 из докуентации к API по совету наставника
    ({}, 400), #Код ответа выдает 400 или 504 вне зависимости от написанного кода. Я оставил ожидаемое значение 400 из докуентации к API по совету наставника
])
def test_login_courier_missing_fields(payload, expected_status_code):
    response = login_courier.send_login_request(payload)

    assert response.status_code == expected_status_code, (
        f"Ожидался статус код {expected_status_code}, но получен {response.status_code}."
    )


@pytest.mark.parametrize("login, password, expected_status_code", [
    ("nonexistent_user", "wrong_password", 404),
])
def test_login_courier_nonexistent_user(login, password, expected_status_code):
    payload = {
        "login": login,
        "password": password
    }

    response = login_courier.send_login_request(payload)

    assert response.status_code == expected_status_code, (
        f"Ожидался статус код {expected_status_code}, но получен {response.status_code}."
    )


def test_login_courier_successful(register_courier):
    login = register_courier["login"]
    password = register_courier["password"]
    payload = {
        "login": login,
        "password": password
    }

    response = login_courier.send_login_request(payload)

    response_data = response.json()
    assert "id" in response_data, "Ответ не содержит id."


