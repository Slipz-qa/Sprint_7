import pytest
import requests
from api_test.data import BASE_URL, ORDERS_URL


class TestOrderRetrieval:
    @pytest.mark.parametrize("courier_id", [1, 2])
    def test_get_orders_with_courier_id(self, register_courier, courier_id):
        courier = register_courier

        url = f'{BASE_URL}{ORDERS_URL}'
        params = {"courierId": courier['id']}
        print(f"Requesting URL: {url} with params: {params}")

        response = requests.get(url, params=params)

        assert response.status_code == 200, f"Ошибка при получении заказов: {response.status_code}, {response.text}"

        try:
            response_data = response.json()
        except ValueError as e:
            assert False, f"Ошибка при декодировании JSON: {e}. Ответ: {response.text}"

        assert "orders" in response_data, "Ответ не содержит список заказов."
        assert isinstance(response_data["orders"], list), "orders не является списком."

