import requests
from api_test.data import BASE_URL, COURIERS_URL, LOGIN_URL


class LoginCourier:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def send_login_request(self, payload):
        response = requests.post(f'{self.base_url}{LOGIN_URL}', json=payload)
        return response

    @staticmethod
    def check_response_body(response, expected_response):
        assert response.json() == expected_response, (
            f"Ожидался ответ {expected_response}, но получен {response.json()}."
        )

    def send_create_request(self, courier_data):
        url = f"{self.base_url}{COURIERS_URL}"
        response = requests.post(url, json=courier_data)
        return response


    @staticmethod
    def generate_unique_login():
        return f"user_{LoginCourier.generate_random_string(5)}"  # Например, "user_abcde"

    @staticmethod
    def create_courier_payload(courier_data):
        return {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data.get("firstName", "")
        }

    @staticmethod
    def check_response_status(response, expected_status_code):
        assert response.status_code == expected_status_code, (
            f"Ожидался код {expected_status_code}, но получен {response.status_code}"
        )

    @staticmethod
    def create_courier_with_login(courier_data):
        payload = LoginCourier.create_courier_payload(courier_data)
        response = LoginCourier.send_create_request(payload)
        if response.status_code == 201:
            return courier_data["login"]
        return None

