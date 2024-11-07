
import pytest
from api_test.methods import create_courier_payload, send_create_courier_request, check_response_status, check_response_body, create_courier_with_login, generate_random_string


@pytest.fixture
def create_courier():
    payload = {
        "login": generate_random_string(10),
        "password": "password123",
        "firstName": "Artem"
    }
    return create_courier_with_login(payload)


class TestCourier:

    def test_create_courier(self, register_courier, cleanup_courier):
        assert register_courier is not None, "Курьер не был создан."
        assert "id" in register_courier, "Не удалось получить ID курьера."

    def test_create_duplicate_courier(self, register_courier):
        payload = create_courier_payload(register_courier)

        response = send_create_courier_request(payload)

        assert response.status_code == 409, f"Ожидался код ошибки 409, но получен: {response.status_code}. Сообщение: {response.json()}"

    @pytest.mark.parametrize("payload, expected_status_code", [
        ({"password": "password123"}, 400),
        ({"login": "johndoe"}, 400),
        ({"login": generate_random_string(10), "password": "password123"}, 201)
    ])
    def test_create_courier_missing_fields(self, payload, expected_status_code):
        response = send_create_courier_request(payload)
        check_response_status(response, expected_status_code)

    @pytest.mark.parametrize("payload, expected_status_code, expected_response", [
        ({"login": generate_random_string(10), "password": "password123", "firstName": "John"}, 201, {"ok": True}),
        ({"password": "password123", "firstName": "John"}, 400, None),
        ({"login": "john_doe", "firstName": "John"}, 400, None),
    ])
    def test_create_courier_response_code(self, payload, expected_status_code, expected_response):
        response = send_create_courier_request(payload)
        check_response_status(response, expected_status_code)

        if expected_response is not None:
            check_response_body(response, expected_response)

    @pytest.mark.parametrize("payload, expected_status_code, expected_response", [
        ({"password": "password123"}, 400, {"code": 400, "message": "Недостаточно данных для создания учетной записи"}),
        ({"login": "johndoe"}, 400, {"code": 400, "message": "Недостаточно данных для создания учетной записи"}),
        ({"firstName": "John"}, 400, {"code": 400, "message": "Недостаточно данных для создания учетной записи"}),
    ])
    def test_create_courier_missing_fields_error_message(self, payload, expected_status_code, expected_response):
        response = send_create_courier_request(payload)
        check_response_status(response, expected_status_code)
        check_response_body(response, expected_response)

    @pytest.mark.parametrize("payload, expected_status_code, expected_response", [
        ({"login": generate_random_string(10), "password": "password123", "firstName": "John"}, 201, {"ok": True}),
        ({"login": "duplicate_login", "password": "password123", "firstName": "Jane"}, 409, {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}),
    ])
    def test_create_courier_with_existing_login(self, payload, expected_status_code, expected_response):
        if expected_status_code == 201:

            login = create_courier_with_login(payload)


            duplicate_payload = {"login": login, "password": "another_password", "firstName": "Different"}
            response = send_create_courier_request(duplicate_payload)
            check_response_status(response, 409)
            check_response_body(response, {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."})















